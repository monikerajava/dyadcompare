from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher


@dataclass(frozen=True)
class ComparisonRow:
    """Uma linha alinhada da comparação, com números de linha opcionais."""

    left_line: int | None
    left_text: str | None
    right_line: int | None
    right_text: str | None
    kind: str


def compare_text(
    original: list[str],
    compared: list[str],
    *,
    ignore_whitespace: bool = False,
    ignore_case: bool = False,
    ignore_blank_lines: bool = False,
) -> list[ComparisonRow]:
    """Alinha linhas mantendo o texto original, com opções de normalização."""
    def normalized(line: str) -> str:
        value = line
        if ignore_whitespace:
            value = "".join(value.split())
        if ignore_case:
            value = value.casefold()
        return value

    left_indices = [i for i, line in enumerate(original) if not (ignore_blank_lines and not line.strip())]
    right_indices = [i for i, line in enumerate(compared) if not (ignore_blank_lines and not line.strip())]
    left = [normalized(original[i]) for i in left_indices]
    right = [normalized(compared[i]) for i in right_indices]
    matcher = SequenceMatcher(a=left, b=right, autojunk=False)
    result: list[ComparisonRow] = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            for offset in range(i2 - i1):
                result.append(
                    ComparisonRow(left_indices[i1 + offset] + 1, original[left_indices[i1 + offset]], right_indices[j1 + offset] + 1, compared[right_indices[j1 + offset]], "equal")
                )
            continue

        if tag == "delete":
            for index in range(i1, i2):
                source = left_indices[index]
                result.append(ComparisonRow(source + 1, original[source], None, None, "delete"))
            continue

        if tag == "insert":
            for index in range(j1, j2):
                source = right_indices[index]
                result.append(ComparisonRow(None, None, source + 1, compared[source], "insert"))
            continue

        left_count, right_count = i2 - i1, j2 - j1
        for offset in range(max(left_count, right_count)):
            left_index = i1 + offset if offset < left_count else None
            right_index = j1 + offset if offset < right_count else None
            result.append(
                ComparisonRow(
                    left_indices[left_index] + 1 if left_index is not None else None,
                    original[left_indices[left_index]] if left_index is not None else None,
                    right_indices[right_index] + 1 if right_index is not None else None,
                    compared[right_indices[right_index]] if right_index is not None else None,
                    "replace",
                )
            )

    return result
