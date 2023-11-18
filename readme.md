Todo: 
1. Automatically retrieve & cache geolocation

Limitations: 
1. For places search, we limit to the top 5 closest locations. This is to reduce context.

Other considerations: 
1. Add exponential backoff to GPT call
2. Token length for gpt4 vision
3. Do not want to keep overwriting audio files. You may want to delete them at the end. 

Some other notes: 
1. Location invoked each time "analyze" button is clicked