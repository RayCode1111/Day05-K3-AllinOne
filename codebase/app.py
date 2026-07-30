"""Nova — Student Command Center (prototype dữ liệu giả, không gọi AI/API)."""

import os
from pathlib import Path

from dotenv import load_dotenv
import streamlit as st

APP_DIR = Path(__file__).resolve().parent
load_dotenv(APP_DIR / ".env")

if os.getenv("APP_ENV", "development") not in {"development", "production"}:
    raise RuntimeError("APP_ENV must be development or production.")
if os.getenv("APP_DATA_MODE", "mock") != "mock":
    raise RuntimeError("This prototype only supports APP_DATA_MODE=mock.")

st.set_page_config(page_title="Nova — Student Command Center", page_icon="✦", layout="wide")

TASKS = [
    {"id": "spec", "title": "Nộp AI Spec — bản chốt của nhóm", "detail": "Hạn 23:59 hôm nay · Ước tính 45 phút", "tag": "Cần làm ngay", "class": "urgent", "source": "Discord #thong-bao"},
    {"id": "standup", "title": "Điền daily stand-up", "detail": "Mất khoảng 3 phút · Cập nhật tiến độ cho team", "tag": "Hôm nay", "class": "today", "source": "Discord #daily-standup"},
    {"id": "workshop", "title": "Tham gia workshop: Review AI Spec", "detail": "15:00–16:30 · Online · Chuẩn bị 3 câu hỏi", "tag": "15:00", "class": "today", "source": "VLearn Calendar"},
    {"id": "reading", "title": "Đọc tài liệu Day 2 — Problem framing", "detail": "VLearn · Hoàn thành lúc 10:12", "tag": "Đã xong", "class": "done", "source": "VLearn"},
]

SOURCES = [
    ("Discord", "Thông báo chốt AI Spec", "#thong-bao · 13:08 hôm nay", "https://discord.com"),
    ("VLearn", "Workshop Review AI Spec", "Lịch học · cập nhật 09:30 hôm nay", "https://vlearn.vn"),
    ("Discord", "Daily stand-up — kênh nhóm", "#daily-standup · 09:00 hôm nay", "https://discord.com"),
]

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
  div[data-testid="stRadio"] > div {gap:7px} div[data-testid="stRadio"] label {background:#fff;border:1px solid #e1e5ef;border-radius:9px;padding:7px 12px;margin:0!important;font-size:13px;font-weight:750} div[data-testid="stRadio"] label:has(input:checked){background:#eeeaff;border-color:#d8d1ff;color:#5144c6}
  div[data-testid="stButton"] button{border-radius:9px;font-weight:750} [data-testid="stSidebar"] .stRadio label{background:transparent;border:0;padding:6px 2px}
</style>
""", unsafe_allow_html=True)

for task in TASKS:
    st.session_state.setdefault(f"done_{task['id']}", task["id"] == "reading")


def task_row(task: dict, completed: bool) -> None:
    """A task is rendered in exactly one list, based on its current checkbox state."""
    check, body, badge = st.columns([0.45, 6.7, 1.25], vertical_alignment="top")
    with check:
        st.checkbox("Hoàn thành", key=f"done_{task['id']}", label_visibility="collapsed")
    with body:
        title_style = "text-decoration:line-through;color:#9ba3b3" if completed else ""
        st.markdown(
            f'<div class="task-title" style="{title_style}">{task["title"]}</div>'
            f'<div class="task-detail">{task["detail"]}</div>'
            f'<div class="task-source">{task["source"]} ↗</div>',
            unsafe_allow_html=True,
        )
    with badge:
        label = "Đã xong" if completed else task["tag"]
        css_class = "done" if completed else task["class"]
        st.markdown(f'<div class="badge {css_class}">{label}</div>', unsafe_allow_html=True)
    st.divider()


def task_lists(compact: bool = False) -> None:
    pending = [task for task in TASKS if not st.session_state[f"done_{task['id']}"]]
    done = [task for task in TASKS if st.session_state[f"done_{task['id']}"]]
    st.markdown('<div class="section-title">Việc cần làm</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub">{len(pending)} việc đang chờ · sắp theo hạn và mức ảnh hưởng</div>', unsafe_allow_html=True)
    if pending:
        for task in pending:
            task_row(task, completed=False)
    else:
        st.success("Bạn đã hoàn thành toàn bộ việc hôm nay.")
    if not compact:
        st.markdown('<div class="section-title" style="margin-top:17px">Đã hoàn thành</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sub">{len(done)} việc · bỏ tick để đưa việc trở lại danh sách cần làm</div>', unsafe_allow_html=True)
        for task in done:
            task_row(task, completed=True)


with st.sidebar:
    st.markdown('<div class="brand"><b>✦</b> nova</div>', unsafe_allow_html=True)
    st.markdown('<div class="eyebrow">Tổng quan hôm nay</div>', unsafe_allow_html=True)
    total_done = sum(st.session_state[f"done_{task['id']}"] for task in TASKS)
    st.progress(total_done / len(TASKS), text=f"{total_done}/{len(TASKS)} việc hoàn thành")
    st.divider()
    st.markdown('<div class="sidebar-status"><span class="green">●</span> 3 nguồn đang đồng bộ<br>Discord · VLearn · Calendar</div>', unsafe_allow_html=True)
    st.divider()
    if st.button("Khôi phục danh sách mẫu", use_container_width=True):
        for task in TASKS:
            st.session_state[f"done_{task['id']}"] = task["id"] == "reading"
        st.rerun()

header, avatar = st.columns([14, 1])
with header:
    st.markdown('<div class="eyebrow">Thứ tư, 30 tháng 7</div><div class="title">Chào Linh, hôm nay mình cùng xử lý 3 việc nhé.</div>', unsafe_allow_html=True)
with avatar:
    st.markdown("<div style='background:#17223a;color:white;border-radius:50%;width:37px;height:37px;display:grid;place-items:center;font-size:12px;font-weight:800'>LN</div>", unsafe_allow_html=True)

page = st.radio("Điều hướng", ["Hôm nay", "Công việc của tôi", "Nguồn thông tin"], horizontal=True, label_visibility="collapsed")
st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

if page == "Hôm nay":
    left, right = st.columns([1.65, .85], gap="large")
    with left:
        st.markdown("""<div class="card hero"><h2>Nova đã rà soát thông tin mới</h2><p>Một deadline có rủi ro cao và một hoạt động bạn chưa xác nhận. Phương án tốt nhất: nộp AI Spec trước, check-in stand-up sau đó, rồi vào workshop đúng giờ.</p><span class="chip">⚠ Deadline còn 5 giờ 40 phút</span><span class="chip">◉ Chưa check-in stand-up</span><span class="chip">✓ 2 việc đã hoàn thành</span></div>""", unsafe_allow_html=True)
        task_lists(compact=False)
        if st.button("↻ Rà soát dữ liệu mẫu", use_container_width=True):
            st.toast("Đã rà soát 7 cập nhật mẫu. Thứ tự ưu tiên không đổi.")
    with right:
        st.markdown("""<div class="card next"><div class="eyebrow" style="color:#bd6826">Việc kế tiếp</div><div class="next-time">14:45</div><h3>Chuẩn bị workshop</h3><p>Mở AI Spec, ghi sẵn 3 điểm nhóm đang phân vân. Lời nhắc sẽ xuất hiện trước 15 phút.</p></div>""", unsafe_allow_html=True)
        if st.button("Chuẩn bị ngay →", type="primary", use_container_width=True):
            st.toast("Đã tạo lời nhắc chuẩn bị workshop lúc 14:45.")
        st.markdown("""<div class="card"><div class="section-title">Kế hoạch đề xuất</div><div class="plan"><b>1. Nộp AI Spec trước</b><p>Deadline cứng, rủi ro cao nhất.</p></div><div class="plan"><b>2. Điền daily stand-up</b><p>Mất 3 phút để cập nhật team.</p></div><div class="plan"><b>3. Vào workshop đúng giờ</b><p>Đem theo 3 câu hỏi cần review.</p></div></div>""", unsafe_allow_html=True)

elif page == "Công việc của tôi":
    metric_1, metric_2, metric_3 = st.columns(3)
    pending_count = sum(not st.session_state[f"done_{task['id']}"] for task in TASKS)
    done_count = len(TASKS) - pending_count
    metric_1.markdown(f'<div class="metric"><b>{pending_count}</b><span>Việc cần xử lý</span></div>', unsafe_allow_html=True)
    metric_2.markdown('<div class="metric"><b>1</b><span>Deadline cần chú ý</span></div>', unsafe_allow_html=True)
    metric_3.markdown(f'<div class="metric"><b>{done_count}</b><span>Việc đã hoàn thành</span></div>', unsafe_allow_html=True)
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    task_lists(compact=False)

else:
    st.markdown('<div class="section-title">Nguồn thông tin</div><div class="sub">Mỗi việc đều được gắn nguồn để bạn kiểm tra thông báo gốc.</div>', unsafe_allow_html=True)
    for platform, title, meta, url in SOURCES:
        with st.container(border=True):
            icon, text, action, state = st.columns([1, 6, 1.5, 1.4], vertical_alignment="center")
            icon.markdown(f'<div class="badge today">{platform}</div>', unsafe_allow_html=True)
            text.markdown(f'<div class="source-name">{title}</div><div class="source-meta">{meta}</div>', unsafe_allow_html=True)
            action.link_button("Mở bài gốc ↗", url, use_container_width=True)
            state.markdown('<div class="verified">● Đã xác thực</div>', unsafe_allow_html=True)
