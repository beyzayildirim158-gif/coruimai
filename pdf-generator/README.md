# PDF Generator Service

Generates branded PDF dossiers for Instagram analyses. Accepts analysis data from the backend, renders a PDF via PDFKit, and stores the artifact either on S3 or the local filesystem.

## Environment

| Variable | Description |
| --- | --- |
| `PORT` | HTTP port (default `3002`) |
| `PUBLIC_URL` | Base URL for serving generated PDFs (defaults to `http://localhost:3002`) |
| `LOCAL_STORAGE_DIR` | Local folder for PDFs when S3 is not configured |
| `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` | Credentials for S3 uploads |
| `AWS_REGION` | AWS region (default `us-east-1`) |
| `S3_BUCKET` | Target S3 bucket name |

## Scripts

```
npm run dev   # start in watch mode
npm run build # emit JS to dist/
npm start     # run compiled server
```

POST `/generate` with the analysis payload described in the backend README to initiate PDF rendering. Generated PDFs are exposed under `/reports/:file` when using local storage.
