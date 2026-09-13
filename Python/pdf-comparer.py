import sys
import difflib

try:
    from PyPDF2 import PdfReader
except ImportError:
    print("This tool requires PyPDF2. Install it with:")
    print("    pip install PyPDF2 --break-system-packages")
    sys.exit(1)

def extract_text_by_page(pdf_path):
    """Return a list of strings, one per page of text extracted from the PDF."""
    try:
        reader = PdfReader(pdf_path)
    except FileNotFoundError:
        print(f"File not found: {pdf_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Could not read '{pdf_path}': {e}")
        sys.exit(1)

    pages = []
    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text)
    return pages

def get_pdf_path(prompt):
    while True:
        path = input(prompt).strip().strip('"').strip("'")
        if path:
            return path
        print("Please enter a file path.")

def compare_pages(pages_a, pages_b, name_a, name_b):
    max_pages = max(len(pages_a), len(pages_b))
    total_diff_lines = 0
    pages_with_differences = []

    for i in range(max_pages):
        text_a = pages_a[i] if i < len(pages_a) else ""
        text_b = pages_b[i] if i < len(pages_b) else ""

        lines_a = text_a.splitlines()
        lines_b = text_b.splitlines()

        diff = list(difflib.unified_diff(
            lines_a, lines_b,
            fromfile=f"{name_a} (page {i + 1})",
            tofile=f"{name_b} (page {i + 1})",
            lineterm=""
        ))

        if diff:
            pages_with_differences.append(i + 1)
            changed_lines = [line for line in diff if line.startswith(("+", "-")) and not line.startswith(("+++", "---"))]
            total_diff_lines += len(changed_lines)

            print(f"\n=== Page {i + 1} differs ===")
            for line in diff:
                print(line)

    return pages_with_differences, total_diff_lines, max_pages

def main():
    print("=" * 40)
    print("           PDF COMPARE TOOL")
    print("=" * 40)

    path_a = get_pdf_path("Path to first PDF: ")
    path_b = get_pdf_path("Path to second PDF: ")

    print("\nExtracting text...")
    pages_a = extract_text_by_page(path_a)
    pages_b = extract_text_by_page(path_b)

    name_a = path_a.split("/")[-1]
    name_b = path_b.split("/")[-1]

    pages_with_diffs, total_diff_lines, max_pages = compare_pages(pages_a, pages_b, name_a, name_b)

    print("\n" + "=" * 40)
    print("SUMMARY")
    print("=" * 40)
    print(f"{name_a}: {len(pages_a)} page(s)")
    print(f"{name_b}: {len(pages_b)} page(s)")

    if len(pages_a) != len(pages_b):
        print("Note: the PDFs have a different number of pages.")

    if not pages_with_diffs:
        print("\n No text differences found between the two PDFs.")
    else:
        print(f"\n Differences found on {len(pages_with_diffs)} of {max_pages} page(s): {pages_with_diffs}")
        print(f"Total changed lines: {total_diff_lines}")

if __name__ == "__main__":
    main()