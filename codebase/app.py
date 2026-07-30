"""Nova — Student Command Center (prototype dữ liệu giả, không gọi AI/API)."""

import os
import html
import time
from pathlib import Path
from datetime import date

from dotenv import load_dotenv
import streamlit as st
import streamlit.components.v1 as components
from discord_agent import load_announcements, scan

APP_DIR = Path(__file__).resolve().parent
load_dotenv(APP_DIR / ".env")

if os.getenv("APP_ENV", "development") not in {"development", "production"}:
    raise RuntimeError("APP_ENV must be development or production.")
if os.getenv("APP_DATA_MODE", "live") not in {"mock", "live"}:
    raise RuntimeError("APP_DATA_MODE must be mock or live.")

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
  .metric{background:#fff;border:1px solid #e5e9f2;border-radius:13px;padding:13px}.metric b{font-size:23px;letter-spacing:-1px}.metric span{display:block;font-size:11px;color:#68738a;margin-top:3px}
  .section-title{font-size:17px;font-weight:850;margin:0}.sub{font-size:12px;color:#68738a;margin:3px 0 12px}.task-title{font-size:14px;font-weight:800}.task-detail{color:#68738a;font-size:12px;margin-top:3px}.task-source{color:#6456d8;font-size:11px;font-weight:750;margin-top:5px}.badge{font-size:10px;font-weight:850;padding:5px 7px;border-radius:99px;text-align:center;margin-top:4px;white-space:nowrap}.urgent{color:#bd3039;background:#fff0f0}.today{color:#a35718;background:#fff4e9}.done{color:#16825b;background:#eaf9f3}
  .next{background:#fffbf1;border-color:#ffedc4}.next-time{font-size:27px;color:#c56621;font-weight:850;letter-spacing:-1px;margin:3px 0}.next h3{font-size:16px;margin:3px 0}.next p{font-size:12px;color:#68738a;line-height:1.45;margin:4px 0 11px}.plan{border-left:3px solid #ff8a4c;padding-left:11px;margin:12px 0}.plan b{font-size:12px}.plan p{font-size:11px;color:#68738a;line-height:1.4;margin:2px 0}
  .source-name{font-size:13px;font-weight:800}.source-meta{font-size:11px;color:#68738a;margin-top:2px}.verified{font-size:10px;color:#16825b;font-weight:850}.sidebar-status{font-size:12px;color:#68738a;line-height:1.6}.green{color:#20a675}
  .question-box{background:#f7f4ff;border-left:3px solid #7666e9;border-radius:7px;padding:11px 13px;color:#293650;font-size:13px;line-height:1.5;margin:12px 0}
  div[data-testid="stRadio"] > div {gap:7px} div[data-testid="stRadio"] label {background:#fff;border:1px solid #e1e5ef;border-radius:9px;padding:7px 12px;margin:0!important;font-size:13px;font-weight:750} div[data-testid="stRadio"] label:has(input:checked){background:#eeeaff;border-color:#d8d1ff;color:#5144c6}
  div[data-testid="stButton"] button{border-radius:9px;font-weight:750} [data-testid="stSidebar"] .stRadio label{background:transparent;border:0;padding:6px 2px}
</style>
""", unsafe_allow_html=True)

st.session_state.setdefault("agent_result", None)
st.session_state.setdefault("agent_source_count", 0)
st.session_state.setdefault("selected_source", None)
st.session_state.setdefault("focus_task_id", None)
st.session_state.setdefault("focus_end_at", None)
st.session_state.setdefault("completed_task_ids", set())
SOURCE_BY_ID = {item["id"]: item for item in load_announcements()}


def current_tasks() -> list[dict]:
    """Use Gemini output once available; otherwise show transparent sample data."""
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


@st.dialog("Thông báo Discord gốc")
def source_dialog(source_id: str) -> None:
    item = SOURCE_BY_ID.get(source_id)
    if not item:
        st.warning("Không tìm thấy thông báo nguồn trong discord-pack.")
        return
    st.caption(source_id)
    st.text(item["text"])
    if st.button("Đóng", use_container_width=True):
        st.session_state.selected_source = None
        st.rerun()


def hero_content() -> str:
    result = st.session_state.agent_result
    if not result:
        return '<div class="card hero"><h2>Nova sẽ giúp bạn rà soát thông tin</h2><p>Chọn ngày tham chiếu và bấm “Quét Discord bằng Gemini”. Nova sẽ đọc thông báo, kiểm tra căn cứ và chỉ đưa việc đã xác thực vào danh sách.</p><span class="chip">Sẵn sàng quét Discord</span></div>'
    return f'<div class="card hero"><h2>Nova đã rà soát thông tin thành công</h2><p>{result.get("summary", "Nova đã tổng hợp các thông báo quan trọng.")}</p><span class="chip">✓ Đã đọc {st.session_state.agent_source_count} cụm thông báo</span><span class="chip">✓ {len(result.get("action_items", []))} việc có căn cứ</span><span class="chip">⚠ {len(result.get("needs_confirmation", []))} mục cần xác nhận</span></div>'


def plan_content() -> str:
    result = st.session_state.agent_result
    if not result:
        return '<div class="card"><div class="section-title">Kế hoạch đề xuất</div><div class="sub" style="margin-top:8px">Nova sẽ đề xuất kế hoạch phù hợp sau khi hoàn tất rà soát thông báo.</div></div>'
    items = result.get("action_items", [])[:3]
    if not items:
        return '<div class="card"><div class="section-title">Kế hoạch đề xuất</div><div class="sub" style="margin-top:8px">Chưa có việc nào đủ căn cứ để đề xuất. Hãy xem mục cần xác nhận.</div></div>'
    plans = "".join(f'<div class="plan"><b>{index}. {item.get("title", "Việc cần làm")}</b><p>{item.get("detail", "Ưu tiên theo thông báo đã xác thực.")}</p></div>' for index, item in enumerate(items, 1))
    return f'<div class="card"><div class="section-title">Kế hoạch đề xuất</div>{plans}</div>'


def countdown(end_at: float) -> None:
    """Client-side countdown keeps updating without repeatedly calling Gemini."""
    target_ms = int(end_at * 1000)
    components.html(
        f"""<div id="timer" style="font:800 30px Inter,system-ui,sans-serif;color:#5144c6;padding:6px 0">--:--</div>
        <script>
        const target = {target_ms};
        function tick() {{
          const seconds = Math.max(0, Math.ceil((target - Date.now()) / 1000));
          const minutes = String(Math.floor(seconds / 60)).padStart(2, '0');
          const rest = String(seconds % 60).padStart(2, '0');
          document.getElementById('timer').textContent = seconds ? `${{minutes}}:${{rest}}` : 'Đã hết giờ';
        }}
        tick(); setInterval(tick, 1000);
        </script>""",
        height=55,
    )


def task_row(task: dict, completed: bool) -> None:
    """A task is rendered in exactly one list, based on its current checkbox state."""
    check, body, badge = st.columns([0.45, 6.7, 1.25], vertical_alignment="top")
    with check:
        checked = st.checkbox("Hoàn thành", value=completed, key=f"task_toggle_{task['id']}", label_visibility="collapsed")
        set_done(task["id"], checked)
    with body:
        title_style = "text-decoration:line-through;color:#9ba3b3" if completed else ""
        evidence = task.get("evidence", "")
        evidence_html = f'<div class="task-detail">Căn cứ: “{evidence}”</div>' if evidence else ""
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


def task_lists(compact: bool = False) -> None:
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
    if not compact:
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
    st.markdown('<div class="sidebar-status"><span class="green">●</span> 3 nguồn đang đồng bộ<br>Discord · VLearn · Calendar</div>', unsafe_allow_html=True)
    st.divider()
    reference_date = st.date_input("Ngày tham chiếu", value=date(2026, 7, 30), format="DD/MM/YYYY")
    if st.button("Quét Discord bằng Gemini", type="primary", use_container_width=True):
        with st.spinner("Đang đọc thông báo, phân tích và kiểm tra căn cứ…"):
            try:
                st.session_state.agent_result, st.session_state.agent_source_count = scan(reference_date.isoformat())
                st.toast("Đã tạo danh sách việc từ Discord.")
                st.rerun()
            except RuntimeError as error:
                st.error(str(error))
    if st.button("Xoá kết quả quét", use_container_width=True):
        st.session_state.agent_result = None
        st.session_state.agent_source_count = 0
        st.rerun()

header, avatar = st.columns([14, 1])
with header:
    st.markdown('<div class="eyebrow">Thứ tư, 30 tháng 7</div><div class="title">Chào Bro, hôm nay mình cùng hoàn thành công việc nhé!</div>', unsafe_allow_html=True)
with avatar:
    st.markdown("<div style='background:#17223a;color:white;border-radius:50%;width:37px;height:37px;display:grid;place-items:center;font-size:12px;font-weight:800'>LN</div>", unsafe_allow_html=True)

page = st.radio("Điều hướng", ["Hôm nay", "Công việc của tôi", "Cần xác thực"], horizontal=True, label_visibility="collapsed")
st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

if page == "Hôm nay":
    left, right = st.columns([1.65, .85], gap="large")
    with left:
        st.markdown(hero_content(), unsafe_allow_html=True)
        task_lists(compact=False)
    with right:
        pending = [task for task in current_tasks() if not is_done(task)]
        if pending:
            next_task = pending[0]
            st.markdown(f'<div class="card next"><div class="eyebrow" style="color:#bd6826">Việc kế tiếp</div><h3>{next_task["title"]}</h3><p>{next_task["detail"]}</p></div>', unsafe_allow_html=True)
            if st.button("Tập trung vào việc này →", type="primary", use_container_width=True):
                st.session_state.focus_task_id = next_task["id"]
                st.toast("Đã chọn việc ưu tiên trong Công việc của tôi.")
        else:
            st.markdown('<div class="card next"><div class="eyebrow" style="color:#bd6826">Việc kế tiếp</div><h3>Chưa có việc để đề xuất</h3><p>Nova sẽ đề xuất việc ưu tiên sau khi Gemini quét thông báo.</p></div>', unsafe_allow_html=True)
        st.markdown(plan_content(), unsafe_allow_html=True)

elif page == "Công việc của tôi":
    page_tasks = current_tasks()
    if not st.session_state.agent_result:
        st.info("Chưa có công việc nào. Hãy quét Discord bằng Gemini để Nova tạo kế hoạch thực thi cá nhân.")
    else:
        pending = [task for task in page_tasks if not is_done(task)]
        done = [task for task in page_tasks if is_done(task)]
        metric_1, metric_2, metric_3 = st.columns(3)
        metric_1.markdown(f'<div class="metric"><b>{len(pending)}</b><span>Việc còn lại</span></div>', unsafe_allow_html=True)
        metric_2.markdown(f'<div class="metric"><b>{sum(task["tag"] == "Cần làm ngay" for task in pending)}</b><span>Việc cần ưu tiên</span></div>', unsafe_allow_html=True)
        metric_3.markdown(f'<div class="metric"><b>{len(done)}</b><span>Đã hoàn thành</span></div>', unsafe_allow_html=True)
        st.markdown("<div style='height:16px'></div><div class='section-title'>Phiên tập trung</div><div class='sub'>Chọn một việc để Nova giữ trọng tâm cho phiên làm việc hiện tại.</div>", unsafe_allow_html=True)
        if pending:
            options = {task["title"]: task for task in pending}
            selected_title = st.selectbox("Việc đang tập trung", list(options), label_visibility="collapsed")
            selected = options[selected_title]
            duration = st.select_slider("Thời lượng tập trung", options=[15, 25, 45, 60, 90], value=25, format_func=lambda minutes: f"{minutes} phút")
            if st.button(f"Bắt đầu phiên {duration} phút", type="primary"):
                st.session_state.focus_task_id = selected["id"]
                st.session_state.focus_end_at = time.time() + duration * 60
                st.toast(f"Đã bắt đầu phiên tập trung {duration} phút.")
            focused = next((task for task in pending if task["id"] == st.session_state.focus_task_id), selected)
            st.markdown(f'<div class="card"><div class="eyebrow">Đang tập trung</div><div class="section-title">{focused["title"]}</div><div class="sub">{focused["detail"]}</div></div>', unsafe_allow_html=True)
            if st.session_state.focus_task_id == focused["id"] and st.session_state.focus_end_at:
                st.caption("Thời gian còn lại của phiên tập trung")
                countdown(st.session_state.focus_end_at)
            if st.button("Đánh dấu hoàn thành việc đang tập trung"):
                set_done(focused["id"], True)
                st.session_state.focus_task_id = None
                st.session_state.focus_end_at = None
                st.rerun()
        else:
            st.success("Bạn đã hoàn thành các việc Nova xác thực được.")
        st.markdown('<div class="section-title" style="margin-top:18px">Nhật ký hoàn thành</div>', unsafe_allow_html=True)
        if done:
            for task in done:
                st.markdown(f'✓ **{task["title"]}** · {task["source"]}')
        else:
            st.caption("Chưa có việc hoàn thành trong lần quét này.")

else:
    st.markdown('<div class="section-title">Cần xác thực</div><div class="sub">Chỉ hiển thị thông tin thiếu dữ kiện, mâu thuẫn ngày giờ hoặc chưa đủ rõ để Nova đưa vào danh sách việc.</div>', unsafe_allow_html=True)
    result = st.session_state.agent_result
    if not result:
        st.info("Nova sẽ tập hợp các câu hỏi cần xác thực với LabCoach/BTC sau khi bạn quét Discord.")
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

if st.session_state.selected_source:
    source_dialog(st.session_state.selected_source)
