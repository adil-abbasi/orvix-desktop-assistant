from app.word_agent.word_live_agent import open_or_create_document, insert_structured_text

open_or_create_document()

insert_structured_text("""
# Test Document

## 1. Introduction
This is a test paragraph written by Orvix.

## 2. Second Section
This is another test paragraph.
""")