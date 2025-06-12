```json
{
  "crm-pdf-document": {
    "id": "document-id",  // Unique identifier for the document (extracted from file name)
    "title": "Document Title",  // Title of the document (extracted from file name)
    "subtitle": "Document Subtitle",  // Subtitle of the document (if applicable, extracted from file name)
    "date": "YYYY-MM-DD", // Date of the document (extracted from file name, formatted)
    "content": {
      "header": {
        "id": "header-id",  // Unique identifier for the header
        "columns": [
          { "column-id": "activity-id", "label": "Activity ID" },
          { "column-id": "activity-name", "label": "Activity Name" },
          { "column-id": "orig-dur", "label": "Original Duration" },
          { "column-id": "start", "label": "Start" },
          { "column-id": "finish", "label": "Finish" },
          { "column-id": "total", "label": "Total" }
        ]
      },
      "body": [
        {
          "row-id": "row-1",  // Unique identifier for the row
          "data": {
            "activity-id": "12345", // Example data for each column
            "activity-name": "Sample Activity",
            "orig-dur": "2 hours",
            "start": "2024-01-01T09:00:00Z",  // ISO 8601 format for date-time
            "finish": "2024-01-01T11:00:00Z",
            "total": "2 hours"
          }
        },
        {
          "row-id": "row-2",
          "data": {
            "activity-id": "67890",
            "activity-name": "Another Activity",
            "orig-dur": "3 hours",
            "start": "2024-01-02T10:00:00Z",
            "finish": "2024-01-02T13:00:00Z",
            "total": "3 hours"
          }
        }
      ],
      "footer": {
      "page-number": 1, // Current page number
      "total-pages": 10,  // Total number of pages
      "project-title": "Project Title", // Project title
      "project-subtitle": "Project Subtitle", // Project subtitle
      "client-logo": "client-logo.png", // Client logo file name
      "client-name": "Client Name", // Client name
      "legends": [
        { "symbol": "symbol-1", "label": "Legend 1" },
        { "symbol": "symbol-2", "label": "Legend 2" },
        { "symbol": "symbol-3", "label": "Legend 3" }
      ],
      "misc-info": {
        "run-date": "03-Oct-23",  // Run date
        "start-date": "27-May-22",  // Project start date
        "finish-date": "16-Jun-25", // Project finish date
        "data-date": "25-Sep-23"  // Data date
      }
    }
    }
  }
}
```