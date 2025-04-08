import tkinter as tk
from tkinter import ttk

# 수수료율 데이터
fee_rates = {
    "국내 주식": {
        "키움증권": 0.00015,
        "토스증권": 0.00015,
        "카카오페이증권": 0.00015,
        "한국투자증권(뱅키스)": 0.00014,
        "미래에셋증권(다이렉트)": 0.00014,
        "하나증권(피가로)": 0.00014,
        "NH투자증권": 0.00016,
        "신한투자증권": 0.00017,
        "KB증권": 0.00018,
        "기타": 0.00015,
    },
    "미국 주식": {
        "삼성증권": 0.0003,
        "미래에셋증권": 0.0007,
        "키움증권": 0.0007,
        "한국투자증권": 0.0004,
        "NH투자증권": 0.00045,
        "신한투자증권": 0.0005,
        "KB증권": 0.0006,
        "기타": 0.0004,
    }
}

# GUI
root = tk.Tk()
root.title("📈 수익률 계산기")
frame = ttk.Frame(root, padding="15")
frame.grid()

# 시장 선택
ttk.Label(frame, text="시장:").grid(column=0, row=0, sticky="w")
market_combo = ttk.Combobox(frame, values=list(fee_rates.keys()))
market_combo.grid(column=1, row=0)
market_combo.set("국내 주식")

# 증권사 선택
ttk.Label(frame, text="증권사:").grid(column=0, row=1, sticky="w")
broker_combo = ttk.Combobox(frame)
broker_combo.grid(column=1, row=1)

# 수수료율 수동 입력 칸
ttk.Label(frame, text="수수료율(%):").grid(column=0, row=2, sticky="w")
manual_fee_entry = ttk.Entry(frame, width=10)
manual_fee_entry.grid(column=1, row=2)
manual_fee_entry.insert(0, "0.015")
manual_fee_entry.config(state="disabled")

# 매수단가
ttk.Label(frame, text="매수 단가(원):").grid(column=0, row=3, sticky="w")
entry_buy_price = ttk.Entry(frame)
entry_buy_price.grid(column=1, row=3)
entry_buy_price.insert(0, "45000")

# 수량
ttk.Label(frame, text="매수 수량:").grid(column=0, row=4, sticky="w")
entry_quantity = ttk.Entry(frame)
entry_quantity.grid(column=1, row=4)
entry_quantity.insert(0, "1")

# 수익률 결과 출력
result_text = tk.Text(frame, height=20, width=50)
result_text.grid(column=0, row=6, columnspan=3, pady=10)

# 증권사 목록 및 수수료율 설정 함수
def update_broker_list(event=None):
    market = market_combo.get()
    brokers = list(fee_rates[market].keys())
    broker_combo['values'] = brokers
    broker_combo.set(brokers[0])
    update_fee_rate()

def update_fee_rate(event=None):
    market = market_combo.get()
    broker = broker_combo.get()
    if broker == "기타":
        manual_fee_entry.config(state="normal")
    else:
        manual_fee_entry.config(state="disabled")
        rate = fee_rates[market].get(broker, 0.00015)
        manual_fee_entry.delete(0, tk.END)
        manual_fee_entry.insert(0, f"{rate*100:.3f}")

# 수익률 계산 함수
def calculate():
    try:
        buy_price = float(entry_buy_price.get())
        quantity = int(entry_quantity.get())
        market = market_combo.get()
        broker = broker_combo.get()
        fee_rate = float(manual_fee_entry.get()) / 100
        tax_rate = 0.0023 if market == "국내 주식" else 0.0

        exchange_rate = float(entry_exchange_rate.get())
        show_in_usd = usd_toggle.get()

        total_buy = buy_price * quantity
        buy_fee = total_buy * fee_rate

        result_text.delete('1.0', tk.END)
        if market == "미국 주식" and show_in_usd:
            result_text.insert(tk.END, f"🧾 총 매수 금액: ${total_buy / exchange_rate:,.2f} ({buy_price:,.2f}$ x {quantity}개)\n")
        else:
            result_text.insert(tk.END, f"🧾 총 매수 금액: {total_buy:,.0f}원 ({buy_price:,.2f} x {quantity}개)\n")

        result_text.insert(tk.END, f"🏦 시장: {market}, 🏢 증권사: {broker} (수수료율 {fee_rate*100:.3f}%)\n\n")
        result_text.insert(tk.END, f"{'수익률':<5}{'총매도금액':>8}{'실제수익':>13}{'손익절금액[주당])':>15}\n")
        result_text.insert(tk.END, "-" * 40 + "\n")

        for rate in range(-10, 21, 1):
            percent = rate / 100
            target_price = buy_price * (1 + percent)
            total_sell = target_price * quantity
            sell_fee = total_sell * fee_rate
            sell_tax = total_sell * tax_rate
            real_sell = total_sell - sell_fee - sell_tax
            real_profit = real_sell - total_buy

            if market == "미국 주식" and show_in_usd:
                unit_sell_price = real_sell / quantity / exchange_rate
                result_text.insert(
                                        tk.END,
                                        f"{rate:+.0f}%{'':<5}"
                                        f"{f'${real_sell / exchange_rate:,.2f}':<14}"
                                        f"{f'${real_profit / exchange_rate:,.2f}':<14}"
                                        f"{f'${unit_sell_price:,.2f}':<15}\n"
                                    )

            else:
                unit_sell_price = real_sell / quantity
                result_text.insert(
                                    tk.END,
                                    f"{rate:+.0f}%{'':<5}"
                                    f"{f'{real_sell:,.0f}원':<14}"
                                    f"{f'{real_profit:,.0f}원':<14}"
                                    f"{f'{unit_sell_price:,.0f}원':<15}\n"
)
    except ValueError:
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, "💥 숫자 입력이 잘못되었습니다.")


# 버튼
ttk.Button(frame, text="계산하기", command=calculate).grid(column=1, row=5)

# 환율 & USD 출력 여부 (미국 주식일 때만 활성화)
ttk.Label(frame, text="환율 (₩/$):").grid(column=0, row=7, sticky="w")
entry_exchange_rate = ttk.Entry(frame)
entry_exchange_rate.grid(column=1, row=7)
entry_exchange_rate.insert(0, "1350")

usd_toggle = tk.BooleanVar()
usd_toggle.set(False)
usd_checkbox = ttk.Checkbutton(frame, text="💵 결과를 달러로 보기", variable=usd_toggle)
usd_checkbox.grid(column=1, row=8, sticky="w")


# 콤보박스 이벤트 연결
market_combo.bind("<<ComboboxSelected>>", update_broker_list)
broker_combo.bind("<<ComboboxSelected>>", update_fee_rate)

# 초기화
update_broker_list()

# 실행
root.mainloop()