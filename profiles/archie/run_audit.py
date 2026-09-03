import audit_checker
import draft_test

if __name__ == "__main__":
    audit_checker.audit_article(
        draft_test.body, 
        draft_test.title, 
        draft_test.meta_title, 
        draft_test.meta_description
    )
