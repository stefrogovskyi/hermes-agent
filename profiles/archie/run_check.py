import check_script
import draft

errors, wc, ssp = check_script.check_text(draft.title, draft.meta_title, draft.meta_desc, draft.body)
print("Errors:", errors)
print("Word count:", wc)
print("Single sentence paras:", ssp)
