"""Nova — trợ lý chủ động cho học viên: rà soát Discord + đối chiếu bài nộp Codelabs."""

import os
import html
from pathlib import Path
from datetime import date, datetime

from dotenv import load_dotenv
import streamlit as st

import codelab
import discord_store
import discord_agent
from discord_agent import scan

APP_DIR = Path(__file__).resolve().parent
load_dotenv(APP_DIR / ".env")

if os.getenv("APP_ENV", "development") not in {"development", "production"}:
    raise RuntimeError("APP_ENV must be development or production.")
if os.getenv("APP_DATA_MODE", "live") not in {"mock", "live"}:
    raise RuntimeError("APP_DATA_MODE must be mock or live.")

STUDENT_ID = os.getenv("CODELABS_STUDENT_ID", "K3-00123")

st.set_page_config(page_title="Nova — Student Command Center", page_icon="✦", layout="wide")

st.markdown("""
<style>
  .stApp {background:#f7f8fc; color:#192236;}
  [data-testid="stSidebar"] {background:#fff; border-right:1px solid #e7eaf2;}
  /* Chừa vùng an toàn cho toolbar Deploy của Streamlit ở phía trên. */
  .block-container {max-width:1280px; padding-top:5.5rem; padding-bottom:2rem;}
  @media (max-width: 768px) {.block-container {padding-top:4.5rem;}}
  .brand {font-size:28px;font-weight:850;letter-spacing:-1.5px;margin:4px 0 28px}.brand b{color:#6456e8}
  .eyebrow{color:#6456e8;font-size:11px;font-weight:850;letter-spacing:1px;text-transform:uppercase}.title{font-size:29px;font-weight:850;letter-spacing:-1.2px;margin:4px 0 14px}
  .card{background:#fff;border:1px solid #e5e9f2;border-radius:16px;padding:17px 18px;margin-bottom:13px;box-shadow:0 5px 18px rgba(30,48,83,.035)}
  .hero{background:linear-gradient(118deg,#30276f,#5a4fd1 59%,#7681ef);border:0;color:#fff;padding:20px 22px}.hero h2{font-size:18px;margin:0 0 5px}.hero p{font-size:13px;line-height:1.55;margin:0;color:#f0efff}.chip{display:inline-block;border:1px solid rgba(255,255,255,.27);border-radius:99px;padding:5px 8px;margin:13px 4px 0 0;font-size:11px}
  .section-title{font-size:17px;font-weight:850;margin:0}.sub{font-size:12px;color:#68738a;margin:3px 0 12px}.task-title{font-size:14px;font-weight:800}.task-detail{color:#68738a;font-size:12px;margin-top:3px}.task-source{color:#6456d8;font-size:11px;font-weight:750;margin-top:5px}.badge{font-size:10px;font-weight:850;padding:5px 7px;border-radius:99px;text-align:center;margin-top:4px;white-space:nowrap}.urgent{color:#bd3039;background:#fff0f0}.today{color:#a35718;background:#fff4e9}.done{color:#16825b;background:#eaf9f3}
  .next{background:#fffbf1;border-color:#ffedc4}.next h3{font-size:16px;margin:3px 0}.next p{font-size:12px;color:#68738a;line-height:1.45;margin:4px 0 11px}.plan{border-left:3px solid #ff8a4c;padding-left:11px;margin:12px 0}.plan b{font-size:12px}.plan p{font-size:11px;color:#68738a;line-height:1.4;margin:2px 0}
  .lab{border-left:4px solid #e0e4ee}.lab.miss{border-left-color:#e2564f;background:#fff7f6}.lab.ok{border-left-color:#20a675;background:#f4fcf8}.lab h3{font-size:15px;font-weight:850;margin:2px 0 4px}.lab p{font-size:12px;color:#68738a;margin:0;line-height:1.5}
  .sidebar-status{font-size:12px;color:#68738a;line-height:1.6}.green{color:#20a675}
  .question-box{background:#f7f4ff;border-left:3px solid #7666e9;border-radius:7px;padding:11px 13px;color:#293650;font-size:13px;line-height:1.5;margin:12px 0}
  .msg-meta{font-size:11px;color:#68738a;font-weight:700;margin-bottom:4px}
  div[data-testid="stRadio"] > div {gap:7px} div[data-testid="stRadio"] label {background:#fff;border:1px solid #e1e5ef;border-radius:9px;padding:7px 12px;margin:0!important;font-size:13px;font-weight:750} div[data-testid="stRadio"] label:has(input:checked){background:#eeeaff;border-color:#d8d1ff;color:#5144c6}
  div[data-testid="stButton"] button{border-radius:9px;font-weight:750} [data-testid="stSidebar"] .stRadio label{background:transparent;border:0;padding:6px 2px}
</style>
""", unsafe_allow_html=True)

st.session_state.setdefault("agent_result", None)
st.session_state.setdefault("agent_source_count", 0)
st.session_state.setdefault("scanned_ids", set())
st.session_state.setdefault("selected_source", None)
st.session_state.setdefault("completed_task_ids", set())
st.session_state.setdefault("codelab_status", None)
st.session_state.setdefault("scan_error", None)
st.session_state.setdefault("show_discord", False)

MESSAGES = discord_store.all_messages()
SOURCE_BY_ID = {item["id"]: item for item in MESSAGES}
# "Mới" = thông báo vừa được đẩy lên mà Nova chưa đọc ở lần kiểm tra nào — data
# pack là nền có sẵn nên không tính vào đây.
UNREAD = [item for item in MESSAGES if item["origin"] == "inbox" and item["id"] not in st.session_state.scanned_ids]


def current_tasks() -> list[dict]:
    """Chỉ hiển thị việc do Gemini trả về và đã qua guard grounding."""
    result = st.session_state.agent_result
    if not result:
        return []
    style = {"urgent": "urgent", "today": "today", "upcoming": "today"}
    tasks = []
    for item in result.get("action_items", []):
        task_id = "agent_" + str(item.get("id", item.get("title", "task"))).replace(" ", "-")[:40]
        priority = item.get("priority", "today")
        tasks.append({"id": task_id, "title": item.get("title", "Việc cần kiểm tra"), "detail": " · ".join(part for part in [item.get("deadline"), item.get("detail")] if part), "tag": {"urgent": "Cần làm ngay", "today": "Hôm nay", "upcoming": "Sắp tới"}[priority], "class": style[priority], "source": item.get("source_id", "discord-pack"), "evidence": item.get("evidence", "")})
    return tasks


def is_done(task: dict) -> bool:
    return task["id"] in st.session_state.completed_task_ids


def set_done(task_id: str, completed: bool) -> None:
    if completed:
        st.session_state.completed_task_ids.add(task_id)
    else:
        st.session_state.completed_task_ids.discard(task_id)


def refresh_today(reference_date: str) -> None:
    """Một hành động duy nhất kéo về mọi thứ màn Hôm nay cần: Codelabs + Discord.

    Lỗi quét được giữ trong session state chứ không in ngay: màn hình rerun sau
    khi hàm này chạy xong, thông báo in tại chỗ sẽ bị xoá trước khi ai kịp đọc.
    """
    st.session_state.codelab_status = codelab.check_submission(STUDENT_ID, reference_date)
    try:
        st.session_state.agent_result, st.session_state.agent_source_count = scan(reference_date)
        st.session_state.scanned_ids = {item["id"] for item in discord_store.all_messages()}
        st.session_state.scan_error = None
        st.toast("Đã cập nhật Codelabs và danh sách việc từ Discord.")
    except RuntimeError as error:
        st.session_state.agent_result = None
        st.session_state.scan_error = str(error)


@st.dialog("Thông báo Discord gốc")
def source_dialog(source_id: str) -> None:
    item = SOURCE_BY_ID.get(source_id)
    if not item:
        st.warning("Không tìm thấy thông báo nguồn trong kho của Nova.")
        return
    st.caption(f"#{item['channel']} · {item['author']}" + (f" · {item['date']}" if item.get("date") else ""))
    st.text(item["text"])
    if st.button("Đóng", use_container_width=True):
        st.rerun()


@st.dialog("Discord — mô phỏng thông báo mới", width="large")
def discord_dialog(default_date: date) -> None:
    """Cửa sổ đứng thay cho Discord thật: LabCoach/BTC đăng gì, Nova lưu lại cái đó."""
    st.caption("Mô phỏng việc LabCoach đăng tài liệu hoặc BTC đẩy thông báo lên kênh. Nội dung gửi ở đây được lưu vào kho của Nova và sẽ được đọc ở lần “Kiểm tra hôm nay” kế tiếp.")
    names = [channel["name"] for channel in discord_store.CHANNELS]
    picked = st.radio("Kênh", names, horizontal=True, key="discord_channel")
    channel = discord_store.CHANNELS[names.index(picked)]

    with st.form(f"push_{channel['id']}", clear_on_submit=True):
        author_column, date_column = st.columns([1.3, 1])
        author = author_column.text_input("Người gửi", value="Lab Coach")
        posted_at = date_column.date_input("Ngày đăng", value=default_date, format="DD/MM/YYYY")
        text = st.text_area("Nội dung thông báo", height=150, placeholder="VD: Slide ngày 3 đã upload lên vlearn.dev. Bài lab hôm nay đóng đúng 23:59, không mở lại.")
        submitted = st.form_submit_button(f"Đẩy lên #{channel['name']}", type="primary", use_container_width=True)
    if submitted:
        if not text.strip():
            st.warning("Nhập nội dung thông báo trước khi đẩy.")
        else:
            discord_store.add_message(channel["id"], author, text, posted_at.strftime("%d/%m/%Y"))
            st.toast(f"Đã lưu thông báo vào #{channel['name']}.")
            # rerun trong phạm vi fragment: vẽ lại danh sách mà cửa sổ vẫn mở.
            st.rerun(scope="fragment")

    channel_messages = discord_store.messages_of(channel["id"])
    added = [item for item in channel_messages if item["origin"] == "inbox"]
    from_pack = [item for item in channel_messages if item["origin"] == "pack"]
    st.markdown(f'<div class="section-title" style="margin-top:6px">Thông báo trong #{channel["name"]}</div><div class="sub">{len(added)} thông báo mô phỏng · {len(from_pack)} thông báo từ data pack</div>', unsafe_allow_html=True)
    for item in reversed(added):
        with st.container(border=True):
            body, action = st.columns([7, 1.2], vertical_alignment="center")
            body.markdown(f'<div class="msg-meta">{html.escape(item["author"])} · {item["date"]} · {item["id"]}</div>', unsafe_allow_html=True)
            body.text(item["text"])
            if action.button("Xoá", key=f"drop_{item['id']}", use_container_width=True):
                discord_store.delete_message(item["id"])
                st.rerun(scope="fragment")
    if from_pack:
        with st.expander(f"Xem {len(from_pack)} thông báo có sẵn trong data pack"):
            for item in from_pack:
                st.markdown(f'<div class="msg-meta">{item["author"]} · {item["date"]} · {item["id"]}</div>', unsafe_allow_html=True)
                st.text(item["text"])
                st.divider()
    if st.button("Đóng cửa sổ", use_container_width=True):
        st.rerun()


def codelab_card(reference_date: str) -> None:
    """Kết quả gọi API Codelabs: chưa nộp thì đưa thẳng link và nút xác nhận."""
    status = st.session_state.codelab_status
    st.markdown('<div class="section-title">Bài nộp Codelabs</div>', unsafe_allow_html=True)
    if not status:
        st.markdown('<div class="sub">Nova sẽ gọi Codelabs để đối chiếu bạn đã nộp bài của ngày tham chiếu chưa.</div>', unsafe_allow_html=True)
        return
    window = f'Mở {status["open_at"]} · hạn {status["due_at"]} · {status["source"]}'
    if status["submitted"]:
        st.markdown(f'<div class="card lab ok"><h3>✓ Đã nộp — {status["lab_title"]}</h3><p>{window}</p></div>', unsafe_allow_html=True)
        return
    st.markdown(f'<div class="card lab miss"><h3>⚠ Chưa nộp — {status["lab_title"]}</h3><p>{window}. Nộp trước {status["due_at"]} hôm nay, nộp trễ bị trừ điểm theo thông báo của BTC.</p></div>', unsafe_allow_html=True)
    open_column, confirm_column = st.columns(2)
    open_column.link_button("Mở Codelabs để nộp bài ↗", status["url"], use_container_width=True)
    if confirm_column.button("Tôi đã nộp — kiểm tra lại", use_container_width=True):
        with st.spinner("Đang xác nhận với Codelabs…"):
            st.session_state.codelab_status = codelab.confirm_submission(STUDENT_ID, reference_date)
        st.rerun()


def hero_content() -> str:
    result = st.session_state.agent_result
    if not result:
        return '<div class="card hero"><h2>Nova sẽ giúp bạn rà soát thông tin</h2><p>Chọn ngày tham chiếu rồi bấm “Kiểm tra hôm nay”. Nova gọi Codelabs xem bạn đã nộp bài chưa, đọc thông báo Discord, kiểm tra căn cứ và chỉ đưa việc đã xác thực vào danh sách.</p></div>'
    return f'<div class="card hero"><h2>Nova đã rà soát thông tin thành công</h2><p>{result.get("summary", "Nova đã tổng hợp các thông báo quan trọng.")}</p><span class="chip">✓ Đã đọc {st.session_state.agent_source_count} thông báo</span><span class="chip">✓ {len(result.get("action_items", []))} việc có căn cứ</span><span class="chip">⚠ {len(result.get("needs_confirmation", []))} mục cần xác nhận</span></div>'


def plan_content() -> str:
    result = st.session_state.agent_result
    if not result:
        return '<div class="card"><div class="section-title">Kế hoạch đề xuất</div><div class="sub" style="margin-top:8px">Nova sẽ đề xuất kế hoạch phù hợp sau khi hoàn tất rà soát thông báo.</div></div>'
    items = result.get("action_items", [])[:3]
    if not items:
        return '<div class="card"><div class="section-title">Kế hoạch đề xuất</div><div class="sub" style="margin-top:8px">Chưa có việc nào đủ căn cứ để đề xuất. Hãy xem mục cần xác nhận.</div></div>'
    plans = "".join(f'<div class="plan"><b>{index}. {item.get("title", "Việc cần làm")}</b><p>{item.get("detail", "Ưu tiên theo thông báo đã xác thực.")}</p></div>' for index, item in enumerate(items, 1))
    return f'<div class="card"><div class="section-title">Kế hoạch đề xuất</div>{plans}</div>'


def task_row(task: dict, completed: bool) -> None:
    """Mỗi việc chỉ nằm ở đúng một danh sách, theo trạng thái checkbox hiện tại."""
    check, body, badge = st.columns([0.45, 6.7, 1.25], vertical_alignment="top")
    with check:
        checked = st.checkbox("Hoàn thành", value=completed, key=f"task_toggle_{task['id']}", label_visibility="collapsed")
        set_done(task["id"], checked)
    with body:
        title_style = "text-decoration:line-through;color:#9ba3b3" if completed else ""
        evidence = task.get("evidence", "")
        evidence_html = f'<div class="task-detail">Căn cứ: “{html.escape(evidence)}”</div>' if evidence else ""
        st.markdown(
            f'<div class="task-title" style="{title_style}">{task["title"]}</div>'
            f'<div class="task-detail">{task["detail"]}</div>'
            f'<div class="task-source">Nguồn đã xác thực</div>{evidence_html}',
            unsafe_allow_html=True,
        )
        if st.button(f'{task["source"]} ↗', key=f'source_{task["id"]}'):
            st.session_state.selected_source = task["source"]
            st.rerun()
    with badge:
        label = "Đã xong" if completed else task["tag"]
        css_class = "done" if completed else task["class"]
        st.markdown(f'<div class="badge {css_class}">{label}</div>', unsafe_allow_html=True)
    st.divider()


def task_lists() -> None:
    tasks = current_tasks()
    pending = [task for task in tasks if not is_done(task)]
    done = [task for task in tasks if is_done(task)]
    st.markdown('<div class="section-title">Việc cần làm</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub">{len(pending)} việc đang chờ · sắp theo hạn và mức ảnh hưởng</div>', unsafe_allow_html=True)
    if pending:
        for task in pending:
            task_row(task, completed=False)
    else:
        st.info("Nova sẽ điền danh sách việc sau khi rà soát thông báo Discord." if not st.session_state.agent_result else "Bạn đã hoàn thành toàn bộ việc hôm nay.")
    st.markdown('<div class="section-title" style="margin-top:17px">Đã hoàn thành</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub">{len(done)} việc · bỏ tick để đưa việc trở lại danh sách cần làm</div>', unsafe_allow_html=True)
    for task in done:
        task_row(task, completed=True)


with st.sidebar:
    st.markdown('<div class="brand"><b>✦</b> nova</div>', unsafe_allow_html=True)
    st.markdown('<div class="eyebrow">Tổng quan hôm nay</div>', unsafe_allow_html=True)
    sidebar_tasks = current_tasks()
    total_done = sum(is_done(task) for task in sidebar_tasks)
    total = len(sidebar_tasks)
    st.progress(total_done / total if total else 0, text=f"{total_done}/{total} việc hoàn thành")
    st.divider()
    st.markdown(f'<div class="sidebar-status"><span class="green">●</span> 2 nguồn đang đồng bộ<br>Discord ({len(MESSAGES)} thông báo) · Codelabs</div>', unsafe_allow_html=True)
    st.divider()
    reference_date = st.date_input("Ngày tham chiếu", value=date(2026, 7, 30), format="DD/MM/YYYY")
    if st.button("Đặt lại phiên demo", use_container_width=True):
        st.session_state.agent_result = None
        st.session_state.agent_source_count = 0
        st.session_state.scanned_ids = set()
        st.session_state.completed_task_ids = set()
        st.session_state.codelab_status = None
        st.session_state.scan_error = None
        codelab.reset()
        discord_agent.clear_cache()
        st.rerun()

reference_iso = reference_date.isoformat()

header, discord_button, avatar = st.columns([11, 2.6, 0.8], vertical_alignment="center")
with header:
    st.markdown(f'<div class="eyebrow">{reference_date.strftime("%d/%m/%Y")}</div><div class="title">Chào Bro, hôm nay mình cùng hoàn thành công việc nhé!</div>', unsafe_allow_html=True)
with discord_button:
    label = f"💬 Discord · {len(UNREAD)} mới" if UNREAD else "💬 Discord"
    if st.button(label, use_container_width=True):
        st.session_state.show_discord = True
        st.rerun()
with avatar:
    st.markdown("<div style='background:#17223a;color:white;border-radius:50%;width:37px;height:37px;display:grid;place-items:center;font-size:12px;font-weight:800'>LN</div>", unsafe_allow_html=True)

page = st.radio("Điều hướng", ["Hôm nay", "Cần xác thực"], horizontal=True, label_visibility="collapsed")
st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

if page == "Hôm nay":
    left, right = st.columns([1.65, .85], gap="large")
    with left:
        st.markdown(hero_content(), unsafe_allow_html=True)
        action, hint = st.columns([1.1, 1.9], vertical_alignment="center")
        if action.button("Kiểm tra hôm nay", type="primary", use_container_width=True):
            with st.spinner("Đang gọi Codelabs, đọc thông báo Discord và kiểm tra căn cứ…"):
                refresh_today(reference_iso)
            st.rerun()
        if UNREAD and st.session_state.agent_result:
            hint.caption(f"Có {len(UNREAD)} thông báo mới chưa được đọc — kiểm tra lại để Nova cập nhật.")
        elif st.session_state.codelab_status:
            checked_at = datetime.fromisoformat(st.session_state.codelab_status["checked_at"]).astimezone()
            meta = (st.session_state.agent_result or {}).get("meta", {})
            source = "dùng lại kết quả đã lưu, không tốn quota" if meta.get("cached") else meta.get("model", "")
            hint.caption(f"Cập nhật lúc {checked_at.strftime('%H:%M')}" + (f" · {source}" if source else ""))
        if st.session_state.scan_error:
            st.warning(f"Đã lấy được trạng thái Codelabs, nhưng chưa quét được Discord: {st.session_state.scan_error}")
        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
        codelab_card(reference_iso)
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        task_lists()
    with right:
        status = st.session_state.codelab_status
        pending = [task for task in current_tasks() if not is_done(task)]
        if status and not status["submitted"]:
            st.markdown(f'<div class="card next"><div class="eyebrow" style="color:#bd6826">Việc kế tiếp</div><h3>Nộp {status["lab_title"]} trên Codelabs</h3><p>Chưa ghi nhận bài nộp · hạn {status["due_at"]} hôm nay.</p></div>', unsafe_allow_html=True)
        elif pending:
            next_task = pending[0]
            st.markdown(f'<div class="card next"><div class="eyebrow" style="color:#bd6826">Việc kế tiếp</div><h3>{next_task["title"]}</h3><p>{next_task["detail"]}</p></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="card next"><div class="eyebrow" style="color:#bd6826">Việc kế tiếp</div><h3>Chưa có việc để đề xuất</h3><p>Nova sẽ đề xuất việc ưu tiên sau khi kiểm tra Codelabs và quét thông báo.</p></div>', unsafe_allow_html=True)
        st.markdown(plan_content(), unsafe_allow_html=True)

else:
    st.markdown('<div class="section-title">Cần xác thực</div><div class="sub">Chỉ hiển thị thông tin thiếu dữ kiện, mâu thuẫn ngày giờ hoặc chưa đủ rõ để Nova đưa vào danh sách việc.</div>', unsafe_allow_html=True)
    result = st.session_state.agent_result
    if not result:
        st.info("Nova sẽ tập hợp các câu hỏi cần xác thực với LabCoach/BTC sau khi bạn bấm “Kiểm tra hôm nay”.")
    else:
        confirmations = result.get("needs_confirmation", [])
        if not confirmations:
            st.success("Không có thông tin mơ hồ cần xác thực trong lần quét này.")
        for index, item in enumerate(confirmations):
            with st.container(border=True):
                st.warning(item.get("title", "Thông tin chưa rõ"))
                st.caption(f"Căn cứ từ {item.get('source_id', 'discord-pack')}: {item.get('evidence', '')}")
                question = html.escape(item.get("question", "LabCoach/BTC có thể xác nhận giúp mình thông tin này không?"))
                st.markdown(f'<div class="question-box"><b>Câu hỏi gửi LabCoach/BTC</b><br>{question}</div>', unsafe_allow_html=True)
                if st.button(f"Mở thông báo gốc: {item.get('source_id', 'discord-pack')} ↗", key=f"confirm_source_{index}"):
                    st.session_state.selected_source = item.get("source_id")
                    st.rerun()

# Cờ mở cửa sổ chỉ có tác dụng đúng một lượt chạy. Streamlit không báo lại khi
# người dùng đóng dialog bằng nút ✕, nên nếu giữ cờ True thì mọi tương tác sau
# đó (tick hoàn thành một việc chẳng hạn) sẽ làm cửa sổ tự bật lên lại.
if st.session_state.selected_source:
    source_id = st.session_state.selected_source
    st.session_state.selected_source = None
    source_dialog(source_id)
elif st.session_state.show_discord:
    st.session_state.show_discord = False
    discord_dialog(reference_date)
