"""Generate the two bundled synthetic receipt PDFs.

Run:  python samples/generate_samples.py

Produces (text-extractable):
  samples/receipt_sample_1.pdf  — English, USD coffee shop
  samples/receipt_sample_2.pdf  — Japanese, JPY (発行日/小計/消費税/合計)

The content here MUST match the fallback dict in app.py exactly.
All data is synthetic; no real personal data.
"""
import os

from reportlab.lib.pagesizes import A6
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfgen import canvas

HERE = os.path.dirname(os.path.abspath(__file__))

# Register a built-in CJK font so Japanese renders and stays text-extractable.
pdfmetrics.registerFont(UnicodeCIDFont("HeiseiKakuGo-W5"))


def make_english(path: str) -> None:
    c = canvas.Canvas(path, pagesize=A6)
    width, height = A6
    y = height - 30
    lines = [
        ("Helvetica-Bold", 13, "Blue Bottle Coffee"),
        ("Helvetica", 9, "123 Market Street, San Francisco, CA"),
        ("Helvetica", 9, "Date: 2025-03-14"),
        ("Helvetica", 9, "----------------------------------------"),
        ("Helvetica", 9, "Cappuccino            $4.50"),
        ("Helvetica", 9, "Almond Croissant      $3.75"),
        ("Helvetica", 9, "----------------------------------------"),
        ("Helvetica", 9, "Subtotal              $8.25"),
        ("Helvetica", 9, "Tax                   $0.74"),
        ("Helvetica-Bold", 10, "Total                 $8.99"),
        ("Helvetica", 8, "Thank you! Paid in USD"),
    ]
    for font, size, text in lines:
        c.setFont(font, size)
        c.drawString(20, y, text)
        y -= size + 6
    c.showPage()
    c.save()


def make_japanese(path: str) -> None:
    c = canvas.Canvas(path, pagesize=A6)
    width, height = A6
    y = height - 30
    f = "HeiseiKakuGo-W5"
    lines = [
        (f, 13, "さくらカフェ"),
        (f, 9, "東京都渋谷区神南1-2-3"),
        (f, 9, "発行日: 2025-04-02"),
        (f, 9, "----------------------------------------"),
        (f, 9, "ブレンドコーヒー        ￥480"),
        (f, 9, "チーズケーキ            ￥620"),
        (f, 9, "----------------------------------------"),
        (f, 9, "小計                    ￥1,100"),
        (f, 9, "消費税(10%)             ￥110"),
        (f, 11, "合計                    ￥1,210"),
        (f, 8, "ありがとうございました"),
    ]
    for font, size, text in lines:
        c.setFont(font, size)
        c.drawString(20, y, text)
        y -= size + 6
    c.showPage()
    c.save()


def main() -> None:
    make_english(os.path.join(HERE, "receipt_sample_1.pdf"))
    make_japanese(os.path.join(HERE, "receipt_sample_2.pdf"))
    print("Wrote receipt_sample_1.pdf and receipt_sample_2.pdf")


if __name__ == "__main__":
    main()
