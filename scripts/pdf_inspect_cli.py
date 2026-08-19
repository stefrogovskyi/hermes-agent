#!/usr/bin/env python3
"""
CLI wrapper for pdf-inspector (Firecrawl high-speed Rust PDF engine)
Usage:
  pdf-inspect classify <file.pdf>
  pdf-inspect markdown <file.pdf> [--output out.md]
  pdf-inspect text <file.pdf>
"""
import sys, os, json, argparse

try:
    import pdf_inspector
except ImportError:
    print("Error: pdf-inspector is not installed. Run 'pip install pdf-inspector'", file=sys.stderr)
    sys.exit(1)

def cmd_classify(args):
    path = args.path
    if not os.path.exists(path):
        print(f"Error: File not found: {path}", file=sys.stderr)
        sys.exit(1)
    
    res = pdf_inspector.classify_pdf(path)
    print(json.dumps({
        "file": path,
        "classification": str(res),
        "pdf_type": getattr(res, 'pdf_type', 'unknown'),
        "pages": getattr(res, 'pages', 0),
        "confidence": getattr(res, 'confidence', 1.0)
    }, indent=2, ensure_ascii=False))

def cmd_markdown(args):
    path = args.path
    if not os.path.exists(path):
        print(f"Error: File not found: {path}", file=sys.stderr)
        sys.exit(1)
    
    res = pdf_inspector.extract_pages_markdown(path)
    pages = res.pages if hasattr(res, 'pages') else []
    
    full_md = "\n\n---\n\n".join([p.markdown if hasattr(p, 'markdown') else str(p) for p in pages])
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(full_md)
        print(f"✅ Extracted {len(pages)} pages to {args.output}")
    else:
        print(full_md)

def cmd_text(args):
    path = args.path
    if not os.path.exists(path):
        print(f"Error: File not found: {path}", file=sys.stderr)
        sys.exit(1)
    
    text = pdf_inspector.extract_text(path)
    print(text)

def main():
    parser = argparse.ArgumentParser(description="Firecrawl pdf-inspector CLI")
    sub = parser.add_subparsers(dest="command", required=True)
    
    p_cls = sub.add_parser("classify", help="Detect if PDF is TextBased, Scanned, ImageBased or Mixed")
    p_cls.add_argument("path", help="Path to PDF")
    
    p_md = sub.add_parser("markdown", help="Extract position-aware Markdown with tables & headings")
    p_md.add_argument("path", help="Path to PDF")
    p_md.add_argument("-o", "--output", help="Output file path")
    
    p_txt = sub.add_parser("text", help="Extract plain text")
    p_txt.add_argument("path", help="Path to PDF")
    
    args = parser.parse_args()
    if args.command == "classify":
        cmd_classify(args)
    elif args.command == "markdown":
        cmd_markdown(args)
    elif args.command == "text":
        cmd_text(args)

if __name__ == "__main__":
    main()
