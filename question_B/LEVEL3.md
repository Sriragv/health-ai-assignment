breaking my own app to work on resolving them 

Break 1: bad input in the browser


for this, I emptied the Glucose box and typed "abc" in Age, then clicked the button.

the output what user saw was Error: \[object Object]. 

A normal person has no idea what that means so we need to change it.The backend actually did its job. FastAPI checked the input, saw it was invalid, and sent back a 422 error whach had a list of errors like \[Glucose: not a number, Age: not a number]. But the webpage was written to print the error as one simple piece of text. When JavaScript tries to print a list of objects as text, it just shows \[object Object]. So the backend was right and the frontend was displaying it badly.



The fix: I changed index.html to go through the list and print each problem on its own line as "field name: message".

After this, the user sees "Please fix: Glucose: Input should be a valid number", so they know exactly what to correct.



Break 2: missing model file



for this break, I renamed model.joblib to model\_backup.joblib in app.py(in line 24), so the app couldn't find it. This simulates a real situation like someone deleting the file or a failed deployment.when i ran it, the app loads the model the moment it starts, and the original file wasn't there, so Python threw a FileNotFoundError and the whole server refused to start. Not just /predict broke, /stats and the homepage died too, because the server wasn't running at all. One missing file took down everything.there was no response on the homepage.



The fix: i tried it in two parts

try/except around loading the model: "try to load it; if the file isn't found, don't crash, just remember the model is missing (model = None) and print a warning."

In /predict, check first: "if there's no model, return a 503 error with a clear message." 503 means "service temporarily unavailable", which is the correct code for "the server is up, but this feature can't work right now."

After this, the server starts and prints a WARNING, /predict politely says the model isn't available, and /stats still works (your terminal shows 503 for predict and 200 for stats).

Limitations I noticed: the page shows "Please fix" before the 503 message, but the user can't fix a missing model. That wording only makes sense for input errors.



100 users at once



Right now the app is one process handling requests one after another, so it takes one requst at a time and goes to another. in order to increase this number, we need to get more workers run uvicorn app:app --workers 4. four copies of the app handle requests in parallel.

Model loaded once: the app loads the model at startup, not on every request. That's already good, because loading a file 100 times per second would be very slow.

SQLite problem: SQLite lets only one write at a time. If 100 users submit at once, each insert waits for the previous one, like 100 people sharing one pen. The fix is to switch to PostgreSQL, which is built for simultaneously wrinting multiple users data, and use a connection pool: a set of ready-made database connections reused instead of opening a new one every request. A smaller fix is SQLite's "WAL mode", which handles reads and writes together better.

Protection:

Rate limiting: stop one user from spamming 1000 requests.

Timeouts: don't let one slow request hold things up forever.

Test before trusting it: use a load-testing tool like Locust to simulate 100 users and see where it actually breaks, instead of guessing.

