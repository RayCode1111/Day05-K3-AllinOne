"""Bản tin Discord cho học viên đã tắt thông báo — prototype Working.

    streamlit run codebase/app.py

Bốn đường đi trải nghiệm đều bấm được trong màn hình này:
  · Happy          — mục có căn cứ, trích dẫn nguyên văn, bấm mở được tin gốc
  · Low-confidence — khu "Chưa chắc — nên hỏi TA", agent không khẳng định
  · Failure        — huy hiệu 🛡️ khi guard hạ cấp vì agent định bịa căn cứ
  · Correction     — "Không đúng ý mình" ghi phản hồi vào logs/feedback.jsonl
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

CODEBASE = Path(__file__).resolve().parent
if str(CODEBASE) not in sys.path:
    sys.path.insert(0, str(CODEBASE))

import streamlit as st

import corpus
from digest import NHAN, TRAN_MUC, dung_ban_tin, ket_xuat_markdown
from run_eval import NGAY_THAM_CHIEU
from triage import phan_loai_ngay

FEEDBACK_LOG = CODEBASE / "logs" / "feedback.jsonl"

st.set_page_config(page_title="Bản tin khoá học", page_icon="🔔", layout="centered")


def ghi_feedback(loai: str, msg_id: str, noi_dung: str = "") -> None:
    """LEARN — vòng cuối của note.txt. 👍👎 kèm 'sai chỗ nào' (HAX G15)."""
    FEEDBACK_LOG.parent.mkdir(parents=True, exist_ok=True)
    with FEEDBACK_LOG.open("a", encoding="utf-8") as handle:
        handle.write(
            json.dumps(
                {
                    "thoi_diem": datetime.now().astimezone().isoformat(timespec="seconds"),
                    "loai": loai,
                    "msg_id": msg_id,
                    "noi_dung": noi_dung,
                },
                ensure_ascii=False,
            )
            + "\n"
        )


def khoi_tao_state() -> None:
    st.session_state.setdefault("ket_luan", None)
    st.session_state.setdefault("meta", None)
    st.session_state.setdefault("da_bo_qua", set())
    st.session_state.setdefault("dang_sua", None)


khoi_tao_state()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.subheader("Chạy agent")
    ten_corpus = st.selectbox(
        "Ngày cần tổng hợp",
        list(corpus.BO_CORPUS),
        format_func=lambda t: {"ngay-thuong": "30/07 — ngày học bình thường",
                               "tin-hiem": "31/07 — ngày có tin hiểm"}.get(t, t),
    )
    messages, meta_corpus = corpus.nap(ten_corpus)
    st.caption(f"{len(messages)} tin · {meta_corpus['loai_du_lieu']}")

    if st.button("▶️ Quét ngày này", type="primary", use_container_width=True):
        with st.spinner("Đang gọi AI phân loại…"):
            try:
                ds, meta = phan_loai_ngay(
                    messages, NGAY_THAM_CHIEU[ten_corpus], ten_lo=f"app-{ten_corpus}"
                )
                st.session_state.ket_luan = ds
                st.session_state.meta = meta
                st.session_state.da_bo_qua = set()
            except SystemExit as loi:
                st.error(str(loi))
            except Exception as loi:  # noqa: BLE001 — hiện lỗi thật cho người demo
                st.error(f"Lời gọi AI thất bại: {loi}")

    if st.session_state.meta:
        m = st.session_state.meta
        st.divider()
        st.caption(
            f"Model `{m['model']}` · {m['do_tre_ms']} ms · prompt `{m['prompt_version']}` · "
            f"guard can thiệp {m['so_lan_guard_can_thiep']} lần"
        )
        if m["id_bi_bo_sot"]:
            st.warning(f"AI bỏ sót {len(m['id_bi_bo_sot'])} tin: {', '.join(m['id_bi_bo_sot'])}")

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🔔 Bản tin khoá học")
# HAX G2 — nói trước phạm vi và giới hạn, đặt kỳ vọng thấp hơn khả năng một chút
st.info(
    "Mình đọc hộ bạn toàn bộ tin trên server và chỉ đẩy lên những việc bạn thật sự phải làm.\n\n"
    "**Mình chỉ tin thông báo từ Giảng viên / TA / Ban tổ chức.** Tin bạn học nói về lịch hay "
    "hạn nộp, mình xếp riêng vào mục *Chưa chắc* để bạn hỏi lại — mình không đoán hộ.",
    icon="ℹ️",
)

if st.session_state.ket_luan is None:
    st.caption("Bấm **Quét ngày này** ở thanh bên để bắt đầu.")
    st.stop()

tin_theo_id = corpus.tin_theo_id()
ban_tin = dung_ban_tin(st.session_state.ket_luan, tin_theo_id)


def ve_muc(muc, nhan: str) -> None:
    kl = muc.ket_luan
    if kl.id in st.session_state.da_bo_qua:
        return

    with st.container(border=True):
        st.markdown(f"**{nhan} · {kl.viec_can_lam or kl.vi_sao}**")

        if kl.han_chot:
            st.markdown(f"⏰ Hạn: `{kl.han_chot}`")
        if kl.trich_dan:
            # HAX G11 — hiện căn cứ ngay cạnh kết luận để user tự kiểm
            st.markdown(f"> 📌 {kl.trich_dan}")
        if kl.co:
            # Đường đi FAILURE — agent định đi quá xa, guard đã kéo lại
            st.warning(
                "🛡️ Guard đã hạ cấp kết luận này: " + ", ".join(kl.co)
                + ". Mình giữ lại nhưng không dám khẳng định.",
                icon="⚠️",
            )

        with st.expander(f"Xem tin gốc · {muc.nguon}"):
            st.markdown(f"`{kl.id}` · **{muc.tin['tac_gia']}** ({muc.tin['vai']}) · {muc.tin['ts']}")
            st.markdown(f"> {muc.tin['noi_dung']}")
            st.caption(f"Vì sao mình xếp mức này: {kl.vi_sao}")

        c1, c2, c3, c4 = st.columns(4)
        # HAX G8 — bỏ qua dễ, không chặn flow
        if c1.button("Bỏ qua", key=f"bo-{kl.id}", use_container_width=True):
            st.session_state.da_bo_qua.add(kl.id)
            ghi_feedback("bo_qua", kl.id)
            st.rerun()
        # HAX G9 — sửa dễ, ngay trên output
        if c2.button("Không đúng ý mình", key=f"sua-{kl.id}", use_container_width=True):
            st.session_state.dang_sua = kl.id
            st.rerun()
        # HAX G15 — feedback có chỗ nói "sai chỗ nào"
        if c3.button("👍", key=f"up-{kl.id}", use_container_width=True):
            ghi_feedback("up", kl.id)
            st.toast("Cảm ơn bạn!")
        if c4.button("👎", key=f"down-{kl.id}", use_container_width=True):
            st.session_state.dang_sua = kl.id
            st.rerun()

        if st.session_state.dang_sua == kl.id:
            with st.form(f"form-{kl.id}"):
                y_kien = st.text_area("Mình sai chỗ nào?", placeholder="VD: cái này không gấp đến thế")
                if st.form_submit_button("Gửi"):
                    ghi_feedback("sua", kl.id, y_kien)
                    st.session_state.dang_sua = None
                    st.success("Đã ghi lại. Nhóm sẽ đọc trong `logs/feedback.jsonl`.")
                    st.rerun()


if ban_tin.ban_ngay:
    st.subheader(f"{NHAN['NGAY']} — xuyên qua chế độ tắt thông báo")
    for muc in ban_tin.ban_ngay:
        ve_muc(muc, NHAN["NGAY"])

if ban_tin.hom_nay:
    st.subheader(NHAN["HOM_NAY"])
    for muc in ban_tin.hom_nay:
        ve_muc(muc, NHAN["HOM_NAY"])

if ban_tin.ghi_nho:
    st.subheader(NHAN["GHI_NHO"])
    for muc in ban_tin.ghi_nho:
        ve_muc(muc, NHAN["GHI_NHO"])

if not ban_tin.tong_hien:
    st.success("Hôm nay không có việc gì bạn phải làm. Nghỉ ngơi đi 🎉")

# Đường đi LOW-CONFIDENCE — agent thừa nhận không chắc thay vì đoán
if ban_tin.can_hoi_ta:
    st.subheader("⚠️ Chưa chắc — nên hỏi TA")
    st.caption("Những tin này mình không đủ căn cứ để khẳng định. Câu hỏi soạn sẵn, bạn copy gửi TA.")
    for muc in ban_tin.can_hoi_ta:
        with st.container(border=True):
            st.markdown(f"`{muc.ket_luan.id}` · {muc.nguon}")
            st.markdown(f"> {muc.tin['noi_dung']}")
            st.code(muc.ket_luan.hoi_ta, language=None)
            if st.button("Đã hỏi TA rồi", key=f"ta-{muc.ket_luan.id}"):
                ghi_feedback("da_hoi_ta", muc.ket_luan.id)
                st.toast("Ghi nhận.")

st.divider()
# HAX G17 — user luôn xem được thứ agent đã giấu đi
with st.expander(f"🟢 Đã lọc bỏ {ban_tin.so_da_loc} tin không cần hành động"):
    st.caption("Agent giấu bớt để bạn không phải mute lần nữa — nhưng bạn luôn mở ra kiểm được.")
    for kl in st.session_state.ket_luan:
        if kl.muc == "BO_QUA":
            tin = tin_theo_id.get(kl.id, {})
            st.markdown(
                f"- `{kl.id}` **{tin.get('tac_gia','?')}**: {tin.get('noi_dung','')[:110]}… "
                f"— *{kl.vi_sao}*"
            )

if ban_tin.so_bi_cat:
    st.caption(
        f"Còn {ban_tin.so_bi_cat} mục nữa bị giữ lại để bản tin không vượt {TRAN_MUC} mục "
        "(luật chống spam)."
    )

with st.expander("📄 Bản tin dạng text — dùng làm ảnh backup khi demo"):
    st.code(ket_xuat_markdown(ban_tin, NGAY_THAM_CHIEU[ten_corpus]), language="markdown")
