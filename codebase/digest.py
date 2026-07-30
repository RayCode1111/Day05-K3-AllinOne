"""ACT — gom kết luận thành bản tin cuối ngày.

Luật chống spam là lý do tồn tại của file này. Khảo sát của nhóm: 7/11 người
đã **tắt thông báo vì bị spam** @everyone/@here, nhưng 8/11 vẫn muốn được báo
khẩn. Bản tin vì thế bị siết cứng: mức NGAY được xuyên qua mute, còn tất cả
phần còn lại gộp vào đúng một bản tin và **không quá TRAN_MUC mục**.
"""

from __future__ import annotations

from dataclasses import dataclass

from triage import KetLuan

TRAN_MUC = 5  # tối đa 5 mục không-khẩn trong một bản tin

NHAN = {
    "NGAY": "🔴 BÁO NGAY",
    "HOM_NAY": "🟠 HÔM NAY",
    "GHI_NHO": "🟡 GHI NHỚ",
    "BO_QUA": "🟢 ĐÃ LỌC",
}


@dataclass
class Muc:
    ket_luan: KetLuan
    tin: dict

    @property
    def nguon(self) -> str:
        return f"{self.tin['kenh']} · {self.tin['tac_gia']} · {self.tin['ts'][11:16]}"


@dataclass
class BanTin:
    ban_ngay: list[Muc]  # xuyên mute
    hom_nay: list[Muc]
    ghi_nho: list[Muc]
    can_hoi_ta: list[Muc]  # độ chắc thấp — chưa dám khẳng định
    so_da_loc: int
    so_bi_cat: int  # bị cắt vì chạm trần chống spam

    @property
    def tong_hien(self) -> int:
        return len(self.ban_ngay) + len(self.hom_nay) + len(self.ghi_nho)


def dung_ban_tin(ket_luan: list[KetLuan], tin_theo_id: dict[str, dict]) -> BanTin:
    muc_theo_cap: dict[str, list[Muc]] = {"NGAY": [], "HOM_NAY": [], "GHI_NHO": [], "BO_QUA": []}
    can_hoi_ta: list[Muc] = []

    for kl in ket_luan:
        tin = tin_theo_id.get(kl.id)
        if tin is None:
            continue
        muc = Muc(kl, tin)
        muc_theo_cap[kl.muc].append(muc)
        # Độ chắc thấp mà vẫn có câu hỏi cho TA -> đưa sang khu "chưa chắc",
        # kể cả khi tin đã bị xếp BO_QUA (yêu cầu ngoài thẩm quyền cũng cần lối ra).
        if kl.do_chac == "thap" and kl.hoi_ta:
            can_hoi_ta.append(muc)

    def sap_xep(ds: list[Muc]) -> list[Muc]:
        return sorted(ds, key=lambda m: (m.ket_luan.han_chot or "9999", m.tin["ts"]))

    ban_ngay = sap_xep(muc_theo_cap["NGAY"])
    con_lai = sap_xep(muc_theo_cap["HOM_NAY"]) + sap_xep(muc_theo_cap["GHI_NHO"])
    giu = con_lai[:TRAN_MUC]
    so_bi_cat = len(con_lai) - len(giu)

    return BanTin(
        ban_ngay=ban_ngay,
        hom_nay=[m for m in giu if m.ket_luan.muc == "HOM_NAY"],
        ghi_nho=[m for m in giu if m.ket_luan.muc == "GHI_NHO"],
        can_hoi_ta=can_hoi_ta,
        so_da_loc=len(muc_theo_cap["BO_QUA"]),
        so_bi_cat=so_bi_cat,
    )


def _dong(muc: Muc) -> str:
    kl = muc.ket_luan
    dong = f"- **{kl.viec_can_lam or kl.vi_sao}**"
    if kl.han_chot:
        dong += f"\n  - ⏰ Hạn: `{kl.han_chot}`"
    if kl.trich_dan:
        dong += f'\n  - 📌 Căn cứ: "{kl.trich_dan}"'
    dong += f"\n  - 🔗 Nguồn: {muc.nguon} (`{kl.id}`)"
    if kl.co:
        dong += f"\n  - 🛡️ Guard: {', '.join(kl.co)}"
    return dong


def ket_xuat_markdown(ban_tin: BanTin, ngay: str) -> str:
    """Bản tin dạng text — dùng cho CLI, log và ảnh chụp backup khi demo."""
    phan: list[str] = [
        f"# Bản tin {ngay}",
        "",
        "> Mình chỉ tổng hợp từ tin đã có trên server. Việc nào chưa đủ căn cứ, "
        "mình xếp riêng ở mục *Chưa chắc* thay vì đoán.",
        "",
    ]

    if ban_tin.ban_ngay:
        phan += [f"## {NHAN['NGAY']} — xuyên qua chế độ tắt thông báo", ""]
        phan += [_dong(m) for m in ban_tin.ban_ngay] + [""]

    if ban_tin.hom_nay:
        phan += [f"## {NHAN['HOM_NAY']}", ""] + [_dong(m) for m in ban_tin.hom_nay] + [""]

    if ban_tin.ghi_nho:
        phan += [f"## {NHAN['GHI_NHO']}", ""] + [_dong(m) for m in ban_tin.ghi_nho] + [""]

    if ban_tin.can_hoi_ta:
        phan += ["## ⚠️ Chưa chắc — nên hỏi TA", ""]
        for m in ban_tin.can_hoi_ta:
            phan.append(f"- `{m.ket_luan.id}` {m.nguon}\n  - 💬 {m.ket_luan.hoi_ta}")
        phan.append("")

    phan += [
        "---",
        f"Đã lọc bỏ **{ban_tin.so_da_loc}** tin không cần hành động."
        + (
            f" Còn **{ban_tin.so_bi_cat}** mục nữa bị giữ lại để bản tin không quá "
            f"{TRAN_MUC} mục — mở app để xem đầy đủ."
            if ban_tin.so_bi_cat
            else ""
        ),
    ]
    return "\n".join(phan)
