from __future__ import annotations

import html
from difflib import SequenceMatcher
from pathlib import Path
import sys

import streamlit as st

ROOT = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.dyadcompare.comparison import ComparisonRow, compare_text  # noqa: E402

st.set_page_config(page_title="DyadCompare", page_icon="⇄", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;600;700;800&display=swap');
:root{--bg:#f2f4f6;--panel:#fff;--ink:#18222d;--muted:#74808c;--line:#d8dee4;--blue:#087e8b;--add:#e2f3e9;--del:#fbe8e5}
.stApp{background:var(--bg);color:var(--ink);font-family:'DM Sans',sans-serif}.block-container{max-width:1500px;padding:1.3rem 2rem 3rem}
#MainMenu,footer{visibility:hidden}.topbar{display:flex;align-items:center;gap:12px;border-bottom:1px solid var(--line);padding:0 0 15px;margin-bottom:18px}
.brand-mark{width:34px;height:34px;border-radius:8px;background:#087e8b;color:white;display:grid;place-items:center;font-size:20px;font-weight:800}
.brand{font-size:1.12rem;font-weight:800;letter-spacing:-.03em}.brand small{display:block;color:var(--muted);font-size:.68rem;font-weight:500;letter-spacing:.02em}
.workspace-title{font-size:1.55rem;font-weight:800;letter-spacing:-.04em;margin:.2rem 0 .15rem}.subtitle{color:var(--muted);font-size:.9rem;margin:0 0 1.15rem}
.file-card{height:100%;background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:13px 16px 7px;box-shadow:0 1px 2px #17212b08}
.file-label{font-weight:700;font-size:.88rem;display:flex;align-items:center;gap:8px;margin-bottom:2px}.file-dot{width:8px;height:8px;border-radius:50%;background:#d28b25}.file-dot.right{background:#18a36e}
.file-hint{font-size:.74rem;color:var(--muted);margin:0 0 .25rem}.toolbar{background:#e8ecef;border:1px solid var(--line);border-radius:9px;padding:8px 12px;margin:12px 0 17px}
.section-label{font-size:.68rem;font-weight:800;text-transform:uppercase;letter-spacing:.11em;color:#66737f;margin:0 0 8px}
.result-bar{display:flex;justify-content:space-between;align-items:center;margin:14px 0 9px}.result-title{font-size:1.05rem;font-weight:800}
.diff-table{border:1px solid #cbd3d9;border-radius:8px;overflow:hidden;background:#fff}.diff-header,.diff-row{display:grid;grid-template-columns:1fr 1fr}
.diff-header{position:sticky;top:0;z-index:2;background:#e9edf0;color:#35424c;font-size:.73rem;font-weight:800}.diff-header div{padding:9px 12px}.diff-header div+div,.diff-cell+.diff-cell{border-left:1px solid #cbd3d9}
.diff-row{min-height:29px;border-top:1px solid #eef0f2}.diff-cell{min-width:0;display:flex;gap:10px;padding:4px 9px;font:12px/1.55 'DM Mono',Consolas,monospace;white-space:pre-wrap;overflow-wrap:anywhere;color:#26323c}
.diff-row.active{outline:2px solid #087e8b;outline-offset:-2px;position:relative;z-index:1}
.line-no{flex:0 0 34px;text-align:right;color:#9aa4ac;user-select:none}.change-left{background:var(--del)}.change-right{background:var(--add)}.empty-cell{background:#f5f6f7}
.inline-left{background:#f4b6ad;color:#622d28;border-radius:2px}.inline-right{background:#9bd7b4;color:#194a31;border-radius:2px}.gap-row{grid-column:1/-1;text-align:center;padding:5px;color:#7a8791;background:#f5f7f8;font:11px 'DM Sans'}
.stats{display:flex;gap:10px;margin:10px 0}.stat{background:#fff;border:1px solid var(--line);border-radius:8px;padding:8px 13px;min-width:104px}.stat b{font-size:1.2rem}.stat span{display:block;font-size:.68rem;color:var(--muted);text-transform:uppercase;letter-spacing:.07em}
.status-card{border:1px solid #a8d6c0;border-radius:8px;background:#e9f6ee;padding:12px 15px;color:#236345;margin:.7rem 0}
.stButton>button{border-radius:6px;border-color:#cbd3d9;font-weight:650}.stButton>button[kind="primary"]{background:#087e8b;border-color:#087e8b}
div[data-testid="stFileUploader"]{margin-top:3px}div[data-testid="stFileUploader"] section{border-radius:6px;border-color:#ccd4da;background:#fafbfc;padding:8px}
div[data-testid="stMetric"]{background:white;border:1px solid var(--line);padding:8px 12px;border-radius:8px}div[data-testid="stMetricLabel"]{font-size:.69rem}
@media(max-width:700px){.block-container{padding:.8rem}.diff-cell{font-size:10px;gap:4px;padding:4px}.line-no{flex-basis:24px}}
</style>""", unsafe_allow_html=True)

st.markdown('<div class="topbar"><div class="brand-mark">⇄</div><div class="brand">DyadCompare<small>COMPARAÇÃO DE ARQUIVOS</small></div></div>', unsafe_allow_html=True)
head_col, theme_col = st.columns([5, 1])
with head_col:
    st.markdown('<div class="workspace-title">Comparar arquivos</div><p class="subtitle">Revise as mudanças lado a lado e navegue por cada diferença.</p>', unsafe_allow_html=True)
with theme_col:
    dark_mode = st.toggle("Tema escuro", value=False)

left_col, right_col = st.columns(2, gap="medium")
st.caption("Privacidade: na versão online, os arquivos são enviados ao servidor para comparação. Evite enviar conteúdo confidencial. Limite: 50 MB por arquivo.")
with left_col:
    st.markdown('<div class="file-card"><div class="file-label"><i class="file-dot"></i>ESQUERDA · ORIGINAL</div><p class="file-hint">Selecione a versão base</p></div>', unsafe_allow_html=True)
    original_file = st.file_uploader("Arquivo original", key="original", label_visibility="collapsed")
with right_col:
    st.markdown('<div class="file-card"><div class="file-label"><i class="file-dot right"></i>DIREITA · MODIFICADO</div><p class="file-hint">Selecione a versão para comparar</p></div>', unsafe_allow_html=True)
    compared_file = st.file_uploader("Arquivo modificado", key="compared", label_visibility="collapsed")

st.markdown('<div class="toolbar"><div class="section-label">Ferramentas de comparação</div></div>', unsafe_allow_html=True)
tool_cols = st.columns([1.25, 1.1, .8, .8, .8, .8], vertical_alignment="bottom")
with tool_cols[0]:
    display_mode = st.selectbox("Visualização", ["Lado a lado", "Unificada", "Lista de alterações"], label_visibility="collapsed")
with tool_cols[1]:
    encoding = st.selectbox("Codificação", ["UTF-8", "Windows-1252"], label_visibility="collapsed")
with tool_cols[2]:
    ignore_whitespace = st.checkbox("Ignorar espaços", help="Diferenças de espaços serão tratadas como iguais.")
with tool_cols[3]:
    ignore_case = st.checkbox("Ignorar maiúsculas")
with tool_cols[4]:
    ignore_blank_lines = st.checkbox("Ignorar linhas vazias")
with tool_cols[5]:
    show_all = st.toggle("Mostrar tudo", value=True)
context_lines = 2
if not show_all:
        context_lines = st.slider("Linhas de contexto", min_value=0, max_value=10, value=2)

def read_uploaded_file(uploaded_file, label: str, codec: str) -> list[str] | None:
    if uploaded_file is None:
        return None
    try:
        decoder = "utf-8-sig" if codec == "UTF-8" else "cp1252"
        return uploaded_file.getvalue().decode(decoder, errors="strict").splitlines()
    except UnicodeDecodeError:
        st.error(f"Could not read **{label}** as {codec}. Check the selected encoding.")
    except OSError as exc:
        st.error(f"Could not read **{label}**: {exc}")
    return None

def inline_diff(text: str, counterpart: str, side: str) -> str:
    left, right = list(text), list(counterpart)
    parts = []
    for tag, i1, i2, j1, j2 in SequenceMatcher(a=left, b=right, autojunk=False).get_opcodes():
        start, end = (i1, i2) if side == "left" else (j1, j2)
        segment = html.escape("".join(left[start:end] if side == "left" else right[start:end]))
        if tag == "equal":
            parts.append(segment)
        elif (side == "left" and tag in ("delete", "replace")) or (side == "right" and tag in ("insert", "replace")):
            css = "inline-left" if side == "left" else "inline-right"
            parts.append(f'<mark class="{css}">{segment}</mark>')
    return "".join(parts) or "&nbsp;"

def render_cell(number, content, kind, counterpart=None, side="left") -> str:
    if content is None:
        return '<div class="diff-cell empty-cell"><span class="line-no"></span><span></span></div>'
    body = inline_diff(content, counterpart, side) if kind == "replace" and counterpart is not None else (html.escape(content) or "&nbsp;")
    css = "diff-cell" + (" change-left" if kind == "delete" else " change-right" if kind == "insert" else "")
    return f'<div class="{css}"><span class="line-no">{number or ""}</span><span>{body}</span></div>'

def rows_with_context(rows: list[ComparisonRow], context: int):
    changed = [i for i, row in enumerate(rows) if row.kind != "equal"]
    if not changed:
        return []
    included = {i for pos in changed for i in range(max(0, pos-context), min(len(rows), pos+context+1))}
    result, previous = [], -1
    for i in sorted(included):
        if i > previous + 1:
            result.append(None)
        result.append(rows[i]); previous = i
    return result

def render_side_by_side(rows, show_all, context, left_name, right_name, focus=None):
    visible = rows if show_all else rows_with_context(rows, context)
    if not visible:
        st.markdown('<div class="status-card">Os arquivos são idênticos. Não há diferenças para exibir.</div>', unsafe_allow_html=True)
        return
    out = [f'<div class="diff-table"><div class="diff-header"><div>◀ &nbsp;{html.escape(left_name)}</div><div>▶ &nbsp;{html.escape(right_name)}</div></div>']
    for row in visible:
        if row is None:
            out.append('<div class="gap-row">··· linhas sem alteração omitidas ···</div>'); continue
        left_kind = "delete" if row.kind in ("delete", "replace") and row.left_text is not None else "equal"
        right_kind = "insert" if row.kind in ("insert", "replace") and row.right_text is not None else "equal"
        paired = row.kind == "replace" and row.left_text is not None and row.right_text is not None
        active = " active" if row is focus else ""
        out.append(f'<div class="diff-row{active}">'+render_cell(row.left_line,row.left_text,"replace" if paired else left_kind,row.right_text,"left")+render_cell(row.right_line,row.right_text,"replace" if paired else right_kind,row.left_text,"right")+'</div>')
    out.append('</div>'); st.markdown("".join(out), unsafe_allow_html=True)

if original_file is None or compared_file is None:
        st.caption("Selecione um arquivo de cada lado para iniciar a comparação.")
else:
    original_lines = read_uploaded_file(original_file, "left file", encoding)
    compared_lines = read_uploaded_file(compared_file, "right file", encoding)
    if original_lines is not None and compared_lines is not None:
        rows = compare_text(original_lines, compared_lines, ignore_whitespace=ignore_whitespace, ignore_case=ignore_case, ignore_blank_lines=ignore_blank_lines)
        changed = [row for row in rows if row.kind != "equal"]
        added = sum(row.kind == "insert" or (row.kind == "replace" and row.left_text is None) for row in changed)
        removed = sum(row.kind == "delete" or (row.kind == "replace" and row.right_text is None) for row in changed)
        replaced = sum(row.kind == "replace" and row.left_text is not None and row.right_text is not None for row in changed)
        st.markdown('<div class="result-bar"><span class="result-title">Resultado da comparação</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stats"><div class="stat"><b>{len(changed)}</b><span>Linhas diferentes</span></div><div class="stat"><b>{added}</b><span>Adicionadas</span></div><div class="stat"><b>{removed}</b><span>Removidas</span></div><div class="stat"><b>{replaced}</b><span>Alteradas</span></div></div>', unsafe_allow_html=True)
        nav1, nav2, nav3 = st.columns([1, 1, 8])
        with nav1:
            if st.button("↑ Anterior", disabled=not changed, use_container_width=True):
                st.session_state.diff_cursor = max(0, st.session_state.get("diff_cursor", 0)-1)
        with nav2:
            if st.button("↓ Próxima", disabled=not changed, use_container_width=True):
                st.session_state.diff_cursor = min(len(changed)-1, st.session_state.get("diff_cursor", 0)+1)
        if changed:
            cursor = min(st.session_state.get("diff_cursor", 0), len(changed)-1)
            st.caption(f"Diferença {cursor+1} de {len(changed)} · linha esquerda {changed[cursor].left_line or '—'} / linha direita {changed[cursor].right_line or '—'}")
        else:
            cursor = 0
        if not changed and display_mode == "Lista de alterações":
            st.markdown('<div class="status-card">Os arquivos são idênticos. Não há diferenças para exibir.</div>', unsafe_allow_html=True)
        if display_mode == "Lado a lado":
            render_side_by_side(rows, show_all, context_lines, original_file.name, compared_file.name, changed[cursor] if changed else None)
        elif display_mode == "Unificada":
            visible = rows if show_all else rows_with_context(rows, context_lines)
            unified = []
            for row in visible:
                if row is None:
                    unified.append("       ··· linhas sem alteração omitidas ···")
                elif row.kind == "equal":
                    unified.append(f"  {row.left_line:>5} {row.left_text}")
                else:
                    if row.left_text is not None:
                        unified.append(f"- {row.left_line or 0:>5} {row.left_text}")
                    if row.right_text is not None:
                        unified.append(f"+ {row.right_line or 0:>5} {row.right_text}")
            st.code("\n".join(unified) if unified else "Arquivos idênticos.", language="diff")
        else:
            for row in changed if not show_all else rows:
                if row.kind == "equal":
                    st.text(f"  {row.left_line:>5}  {row.left_text}")
                else:
                    if row.left_text is not None: st.markdown(f"<div class='diff-cell change-left'>− {row.left_line or '':>5} &nbsp; {html.escape(row.left_text)}</div>", unsafe_allow_html=True)
                    if row.right_text is not None: st.markdown(f"<div class='diff-cell change-right'>+ {row.right_line or '':>5} &nbsp; {html.escape(row.right_text)}</div>", unsafe_allow_html=True)

if dark_mode:
    st.markdown("<style>:root{--bg:#151b22;--panel:#202831;--ink:#e5ebef;--muted:#a2adb6;--line:#39444e;--add:#203c30;--del:#452b2b}.stApp{background:var(--bg);color:var(--ink)}.file-card,.stat,.diff-table{background:var(--panel);border-color:var(--line)}.toolbar,.diff-header{background:#29343e;border-color:var(--line);color:#dce4e9}.diff-cell{color:#e2e8ec;border-color:var(--line)}.diff-row{border-color:#303b44}.empty-cell,.gap-row{background:#252f38;color:#aeb8bf}.stButton>button{background:#252f38;color:#e2e8ec;border-color:#46535e}</style>", unsafe_allow_html=True)
