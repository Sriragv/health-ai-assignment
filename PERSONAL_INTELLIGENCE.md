1\. Missing values: replaced impossible zeros with the median instead of dropping rows.

&#x20;  Insulin had 374 zeros and SkinThickness had 227 out of 768 rows. Dropping them would

&#x20;  lose about half the dataset. Also rejected a pre-cleaned Kaggle version because its

&#x20;  per-class median filling (Insulin = 169.5 vs 102.5) leaked the label.

2\. Learning rate: chose lr=0.1 over lr=0.01. With 0.1 the loss reached its minimum (0.4711)

&#x20;  by epoch 1000. With 0.01 it was still at 0.4834 at epoch 1000 and only reached 0.4712

&#x20;  after 5000 epochs. The 0.01 run had slightly higher accuracy (0.799 vs 0.792), but that

&#x20;  is just 1 patient (FP 9 vs 10) out of 154, so it is noise, not a real improvement.

3\. High risk" threshold: used 0.25 instead of the default 0.5, based on my Question A

&#x20;  Level 3 result (recall 0.926 vs 0.593). A screening app should not miss diabetics.

4\. Missing model file: return a 503 error instead of letting the server crash. My

&#x20;  before-test showed the crash killed every endpoint, including /stats. After the fix,

&#x20;  /stats still returned 200 while /predict returned 503 with a clear message.

&#x20;AI Usage Declaration

\- Claude: explained the assignment, wrote first drafts of the scripts and the FastAPI

&#x20; app, and helped debug PowerShell and git errors. I ran everything myself, checked the

&#x20; numbers, and wrote my Level 3 prediction and conclusions in my own words.

Where the AI was wrong or weak

1\. The HTML page Claude wrote showed "Error: \[object Object]" for bad input. I saw this

&#x20;  when I deliberately broke the app with empty and text input in B Level 3, and fixed

&#x20;  the page to show each field and its error message.

2\. Claude's script assumed my USN ends in 4 digits ("S = last 4 digits"). Mine ends in

&#x20;  I059, so Python gave a NameError. I used the numeric part (59) and documented it.

&#x20;My own catches

\- Noticed my threshold table showed FP=9 at 0.5 instead of 10. I had left lr=0.01 in the

&#x20; file from the learning-rate test, so I fixed it and reran.



