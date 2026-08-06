# Dedicated Official UNEB Primary Leaving Examination (PLE) Template Engine
# Renders 100% authentic UNEB examination paper layouts for Primary 1 to Primary 7

import json
from typing import List, Dict, Any

def render_uneb_primary_html(
    subject: str,
    level: str,
    exam_year: str = "2026",
    duration: str = "2 hours 30 minutes",
    sec_a_count: int = 20,
    sec_a_marks: int = 40,
    sec_b_count: int = 12,
    sec_b_marks: int = 60,
    questions: List[dict] = None
) -> str:
    """Renders full authentic UNEB Primary Leaving Examination HTML paper."""
    if questions is None:
        questions = []

    subj_clean = (subject or "Mathematics").strip()
    is_math = "math" in subj_clean.lower()
    is_ple = "7" in str(level)

    header_title = "PRIMARY LEAVING EXAMINATION" if is_ple else f"{level.upper()} PROMOTIONAL EXAMINATION"
    total_marks = sec_a_marks + sec_b_marks

    # Separate Section A and Section B questions
    sec_a_items = [q for q in questions if q.get("number", 0) <= sec_a_count]
    sec_b_items = [q for q in questions if q.get("number", 0) > sec_a_count]

    # Section A HTML Generation
    sec_a_html_list = []
    for q in sec_a_items:
        q_num = q.get("number", 1)
        q_text = q.get("text", "")
        
        if is_math:
            item_code = f"""
<div class="uneb-q-item" style="margin-bottom: 22px; font-family: Arial, sans-serif; clear: both; overflow: hidden; page-break-inside: avoid;">
  <div style="float: right; width: 145px; border: 1px dashed #000; padding: 6px; text-align: center; font-size: 9px; text-transform: uppercase; color: #444; min-height: 65px; border-radius: 4px; background: #fafafa;">
    Work out here
  </div>
  <div style="margin-right: 160px;">
    <div style="font-size: 14px; line-height: 1.5; margin-bottom: 8px;">
      <b style="font-size: 14.5px; margin-right: 6px;">{q_num}.</b>
      <span>{q_text}</span>
    </div>
    <div style="border-bottom: 1px dotted #555; margin-top: 25px; height: 16px;"></div>
  </div>
</div>"""
        else:
            item_code = f"""
<div class="uneb-q-item" style="margin-bottom: 20px; font-family: Arial, sans-serif; page-break-inside: avoid;">
  <div style="font-size: 14px; line-height: 1.5; margin-bottom: 8px;">
    <b style="font-size: 14.5px; margin-right: 6px;">{q_num}.</b>
    <span>{q_text}</span>
  </div>
  <div style="border-bottom: 1px dotted #555; margin-top: 18px; height: 16px;"></div>
</div>"""
        sec_a_html_list.append(item_code)

    # Section B HTML Generation
    sec_b_html_list = []
    for q in sec_b_items:
        q_num = q.get("number", 21)
        q_text = q.get("text", "")
        q_marks = q.get("marks", 5)
        sub_qs = q.get("sub_questions", [])

        sub_html_list = []
        if sub_qs:
            for sub in sub_qs:
                lbl = sub.get("label", "(a)")
                s_txt = sub.get("text", "")
                s_mks = sub.get("marks", 1)
                mks_str = f"({s_mks} mark)" if s_mks == 1 else f"({s_mks} marks)"
                
                sub_code = f"""
<div style="margin-left: 20px; margin-top: 12px; margin-bottom: 16px;">
  <div style="font-size: 13.5px; line-height: 1.5;">
    <b style="margin-right: 6px;">{lbl}</b>
    <span>{s_txt}</span>
    <span style="float: right; font-weight: bold; font-size: 11.5px; font-style: italic; color: #333;">{mks_str}</span>
  </div>
  <div style="border-bottom: 1px dotted #666; margin-top: 18px; height: 16px;"></div>
  <div style="border-bottom: 1px dotted #666; margin-top: 14px; height: 16px;"></div>
</div>"""
                sub_html_list.append(sub_code)
        else:
            sub_html_list.append("""
<div style="border-bottom: 1px dotted #666; margin-top: 22px; height: 16px;"></div>
<div style="border-bottom: 1px dotted #666; margin-top: 14px; height: 16px;"></div>
<div style="border-bottom: 1px dotted #666; margin-top: 14px; height: 16px;"></div>""")

        sub_combined = "".join(sub_html_list)
        q_mks_str = f"({q_marks} marks)"
        item_b_code = f"""
<div class="uneb-q-item-b" style="margin-bottom: 28px; font-family: Arial, sans-serif; page-break-inside: avoid;">
  <div style="font-size: 14px; line-height: 1.5; margin-bottom: 8px;">
    <b style="font-size: 14.5px; margin-right: 6px;">{q_num}.</b>
    <span>{q_text}</span>
    <span style="float: right; font-weight: bold; font-size: 12px;">{q_mks_str}</span>
  </div>
  {sub_combined}
</div>"""
        sec_b_html_list.append(item_b_code)

    sec_a_combined = "".join(sec_a_html_list)
    sec_b_combined = "".join(sec_b_html_list)

    sec_a_per_q_marks = "two marks each" if is_math else "one mark each"
    sec_b_per_q_marks = "four to six marks each" if is_math else "four to ten marks each"

    full_paper_html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>UNEB PLE - {subj_clean} ({level})</title>
  <style>
    @page {{ size: A4; margin: 15mm; }}
    body {{ font-family: Arial, Helvetica, sans-serif; color: #000; background: #fff; margin: 0; padding: 20px; }}
    .uneb-container {{ max-width: 820px; margin: 0 auto; background: #fff; padding: 25px; border: 1px solid #ccc; border-radius: 4px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }}
    .uneb-border-box {{ border: 2px solid #000; padding: 15px; margin-bottom: 20px; }}
    .uneb-title-banner {{ text-align: center; border-top: 2px solid #000; border-bottom: 2px solid #000; padding: 12px 0; margin-bottom: 18px; }}
    .uneb-instructions {{ border: 2px double #000; padding: 14px 18px; margin-bottom: 25px; font-size: 12px; line-height: 1.6; background: #fff; }}
    .uneb-sec-header {{ text-align: center; border-top: 2px solid #000; border-bottom: 2px solid #000; padding: 8px 0; margin: 25px 0; background: #f8fafc; }}
  </style>
</head>
<body>
  <div class="uneb-container">
    
    <!-- ── 1. CANDIDATE INDEX & DETAILS BOX ── -->
    <div class="uneb-border-box">
      <div style="display: flex; justify-content: space-between; align-items: flex-start;">
        <div>
          <div style="font-size: 11px; font-weight: bold; text-transform: uppercase;">Candidate's Name: _____________________________________________________</div>
          <div style="font-size: 11px; font-weight: bold; text-transform: uppercase; margin-top: 8px;">Candidate's Signature: __________________ District Name: _________________</div>
        </div>
        <div style="border: 1px solid #000; padding: 6px 10px; text-align: center; background: #fff;">
          <div style="font-size: 9px; font-weight: bold; text-transform: uppercase; margin-bottom: 4px; letter-spacing: 0.5px;">Candidate Index Number</div>
          <table style="border-collapse: collapse; font-family: monospace; font-size: 14px; font-weight: bold;">
            <tr>
              <td style="border: 1px solid #000; width: 22px; height: 26px; text-align: center;">U</td>
              <td style="border: 1px solid #000; width: 22px; height: 26px; text-align: center;">&nbsp;</td>
              <td style="border: 1px solid #000; width: 22px; height: 26px; text-align: center;">&nbsp;</td>
              <td style="border: 1px solid #000; width: 22px; height: 26px; text-align: center;">&nbsp;</td>
              <td style="border: 1px solid #000; width: 22px; height: 26px; text-align: center;">&nbsp;</td>
              <td style="border: 1px solid #000; width: 14px; height: 26px; text-align: center;">/</td>
              <td style="border: 1px solid #000; width: 22px; height: 26px; text-align: center;">&nbsp;</td>
              <td style="border: 1px solid #000; width: 22px; height: 26px; text-align: center;">&nbsp;</td>
              <td style="border: 1px solid #000; width: 22px; height: 26px; text-align: center;">&nbsp;</td>
            </tr>
          </table>
        </div>
      </div>
    </div>

    <!-- ── 2. OFFICIAL UNEB TITLE BANNER ── -->
    <div class="uneb-title-banner">
      <h1 style="margin: 0; font-size: 19px; font-weight: 900; text-transform: uppercase; letter-spacing: 0.5px;">UGANDA NATIONAL EXAMINATIONS BOARD</h1>
      <h2 style="margin: 4px 0 0 0; font-size: 15px; font-weight: bold; text-transform: uppercase;">{header_title} {exam_year}</h2>
      <h3 style="margin: 4px 0 0 0; font-size: 17px; font-weight: 900; text-transform: uppercase; color: #000;">{subj_clean.upper()}</h3>
      <div style="font-size: 12.5px; font-weight: bold; margin-top: 5px;">Time Allowed: {duration}</div>
    </div>

    <!-- ── 3. CANDIDATE INSTRUCTIONS BOX ── -->
    <div class="uneb-instructions">
      <div style="font-weight: bold; text-transform: uppercase; text-decoration: underline; margin-bottom: 8px;">Read the following instructions carefully:</div>
      <ol style="margin: 0; padding-left: 20px;">
        <li>This paper is made up of two sections: <b>A</b> and <b>B</b>.</li>
        <li>Section <b>A</b> has {sec_a_count} questions ({sec_a_marks} marks).</li>
        <li>Section <b>B</b> has {sec_b_count} questions ({sec_b_marks} marks).</li>
        <li>Answer <b>ALL</b> questions in both sections.</li>
        <li>All answers must be written using a blue or black ballpoint pen or ink.</li>
        <li>Unnecessary changes of work may lead to loss of marks.</li>
        <li>Any handwriting that cannot be easily read may lead to loss of marks.</li>
      </ol>
    </div>

    <!-- ── 4. SECTION A ── -->
    <div class="uneb-sec-header" style="margin-top: 0;">
      <h3 style="margin: 0; font-size: 15px; font-weight: 900; text-transform: uppercase;">SECTION A: {sec_a_marks} MARKS</h3>
      <div style="font-size: 12px; font-style: italic; margin-top: 2px;">Questions 1 to {sec_a_count} carry {sec_a_per_q_marks}.</div>
    </div>
    <div class="uneb-sec-a-content">
      {sec_a_combined}
    </div>

    <!-- ── 5. SECTION B ── -->
    <div class="uneb-sec-header">
      <h3 style="margin: 0; font-size: 15px; font-weight: 900; text-transform: uppercase;">SECTION B: {sec_b_marks} MARKS</h3>
      <div style="font-size: 12px; font-style: italic; margin-top: 2px;">Questions {sec_a_count + 1} to {sec_a_count + sec_b_count} carry {sec_b_per_q_marks}. All working must be clearly shown in the spaces provided.</div>
    </div>
    <div class="uneb-sec-b-content">
      {sec_b_combined}
    </div>

    <!-- ── 6. END MARKER ── -->
    <div style="text-align: center; margin-top: 40px; padding-top: 15px; border-top: 1px solid #000; font-weight: bold; font-size: 14px; letter-spacing: 2px;">
      END
    </div>

  </div>
</body>
</html>"""
    return full_paper_html
