# astro-cub
Fancy word for the application to build agentic workflows to extract content from pdf documents in specific formats. Utilities to build, test and monitor prompts in the real world.

## Components

- *astrocub* app: flask app to create prompts and store in database (supabase). Run tests & eval.
- workers: serverless workers built for GCP to process the files from GCS.

### API ROUTES 
- /genetl: create prompts to execute a single task. 

### Services 
- Prompt Manager 
- Database manager (supabase client)
- 
