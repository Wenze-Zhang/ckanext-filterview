# ckanext-filterview

A CKAN extension that provides an enhanced DataTables view with advanced filtering capabilities, including support for comparison operators (greater than, less than, equal to) for numeric and date columns.

## Overview

This extension is based on the official CKAN `datatablesview` plugin but extends it with powerful client-side filtering features. The key enhancement is the ability to perform range queries and comparison operations on numeric and date/timestamp columns, whereas the original view only supports exact match (equality) queries.

## Key Features

### Enhanced Filtering Capabilities

- **Comparison Operators**: Support for `=`, `!=`, `>`, `>=`, `<`, `<=` operations on numeric and date columns
- **Empty/Non-empty Checks**: Filter rows based on whether a column has a value or not
- **Client-side Filtering**: Optional client-side filtering for better performance on smaller datasets (up to 10,000 rows by default)

### Original DataTables Features

All the standard features from the official datatablesview are retained:

- Sortable columns with multi-column sorting
- Pagination with customizable page lengths
- Column visibility controls
- Responsive design with mobile support
- State saving (preserves filters, sorting, pagination across sessions)
- Export functionality (CSV, JSON, XML)
- Data dictionary integration
- Internationalization support (80+ languages)

## Installation

1. Clone this repository into local directory:

```bash
mdkir ckan
cd ckan
git clone https://github.com/Wenze-Zhang/ckanext-filterview.git
```

2. Install the extension:
Docker must already be installed. On Linux the repo with docker could run directly, on Windows Docker must be integrated with WSL2.

The extension is running on dev mode.

```bash
cd ckanext-filterview
cp .env.example .env
bin/compose build
bin/install_src
bin/compose up
```


## Usage

### Basic Usage

1. Navigate to a resource that has data in the DataStore
2. Click "Manage" → "Views" 
3. Add a new "Table" view
4. Configure the view options:
   - **Client Side Filtering**: Enable this to use the advanced comparison operators
   - **Client Side Max Rows**: Set the maximum number of rows to load for client-side filtering (default: 10,000)
   
### Using Comparison Operators

When **Client Side Filtering** is enabled:

#### For Numeric Columns:
- Select an operator from the dropdown: `=`, `!=`, `>`, `>=`, `<`, `<=`, `is empty`, `is not empty`
- Enter a value in the input field
- Examples:
  - `> 100` - Show all rows where the value is greater than 100
  - `<= 50.5` - Show all rows where the value is less than or equal to 50.5
  - `between` with value `10,100` - Show all rows where the value is between 10 and 100 (inclusive)

#### For Date/Timestamp Columns:
- Same operators as numeric columns
- Enter dates in `yyyy-mm-dd` format
- Examples:
  - `> 2023-01-01` - Show all rows after January 1, 2023


### Server-side vs Client-side Filtering

The extension supports two filtering modes:

**Server-side Filtering (Default)**:
- Queries are sent to the CKAN DataStore API
- Suitable for large datasets (millions of rows)
- Only supports text-based full-text search
- Does NOT support comparison operators

**Client-side Filtering**:
- All data is loaded into the browser (up to the configured max rows)
- Supports comparison operators and advanced filtering
- Better performance for small to medium datasets (<10,000 rows)
- Real-time filtering without server round-trips

### Architecture Overview

The extension consists of several key components:

```
ckanext-filterview/
├── ckanext/filterview/
│   ├── plugin.py              # CKAN plugin interface
│   ├── blueprint.py           # Flask routes for AJAX endpoints
│   ├── helpers.py             # Template helper functions
│   ├── assets/                # JavaScript and CSS
│   │   ├── datatablesview.js  # Main client-side logic
│   │   └── vendor/            # DataTables library and dependencies
│   ├── templates/             # Jinja2 templates
│   └── public/                # Static files (language files)
```

### Core Implementation Logic

#### 1. Plugin Registration (`plugin.py`)

The `DataTablesView` class implements the CKAN interfaces:

- **IResourceView**: Defines how the view is rendered and what resources it can display
- **IConfigurer**: Registers templates, assets, and configuration
- **IBlueprint**: Registers Flask routes for AJAX data endpoints

```python
class DataTablesView(p.SingletonPlugin):
    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IResourceView, inherit=True)
    p.implements(p.IBlueprint)
```

The view schema defines:
- `client_side_filtering`: Boolean flag to enable advanced filtering
- `client_side_max_rows`: Maximum rows to load for client-side filtering
- `responsive`: Enable responsive layout
- `show_fields`: List of fields to display

#### 2. AJAX Data Endpoints (`blueprint.py`)

Three main endpoints handle data requests:

**a) `/datatables/ajax/<resource_view_id>` (Server-side)**:
- Handles pagination, sorting, and full-text search
- Calls CKAN's `datastore_search` action
- Returns data in DataTables JSON format
- Does NOT support comparison operators

**b) `/datatables/ajax-all/<resource_view_id>` (Client-side)**:
- Loads all records (up to max_rows) at once
- Called when `client_side_filtering` is enabled
- Returns complete dataset for browser-side filtering
- Enables comparison operator functionality

**c) `/datatables/filtered-download/<resource_view_id>`**:
- Handles export of filtered data
- Supports CSV, JSON, XML formats

The `merge_filters()` function combines:
- View filters (configured when creating the view)
- User filters (selected interactively)
- Only allows users to tighten existing filters, not broaden them

#### 3. Client-side Filtering Logic (`datatablesview.js`)

The core filtering implementation uses DataTables' custom search extension:

```javascript
$.fn.dataTable.ext.search.push(function (settings, searchData, dataIndex, rowData) {
    // Iterate through all columns with filters
    for (let ci = 0; ci < gdataDict.length; ci++) {
        const colDef = gdataDict[ci]
        const colname = colDef.id
        const coltype = colDef.type
        
        // Get operator and value from UI
        const $op = $('.dt-col-op[data-colname="' + colname + '"]')
        const $val = $('.dt-filter-val[data-colname="' + colname + '"]')
        const op = $op.val()
        const val = $val.val()
        
        // Type-specific comparison logic
        if (isNumeric) {
            cellVal = parseFloat(raw)
            compareVal = parseFloat(val)
        } else if (isDate) {
            cellVal = new Date(raw).getTime()
            compareVal = new Date(val).getTime()
        }
        
        // Perform comparison based on operator
        switch (op) {
            case 'eq': case '=': 
                if (cellVal !== compareVal) return false
                break
            case 'gt': case '>':
                if (cellVal <= compareVal) return false
                break
            case 'gte': case '>=':
                if (cellVal < compareVal) return false
                break
            // ... other operators
        }
    }
    return true  // Row passes all filters
})
```

**Key Implementation Details**:

1. **Filter UI Generation** (`lines 495-560`):
   - For numeric/date columns with client-side filtering: Creates a dropdown for operators and an input for values
   - For text columns: Creates a single search input
   - Each filter element has data attributes to identify the column

2. **Type Detection**:
   - Numeric: `type === 'numeric' || type === 'int' || type === 'float'`
   - Date: `type.indexOf('timestamp') === 0 || type === 'date'`
   - Text: Everything else

3. **Comparison Logic** (`lines 955-1095`):
   - Converts cell values to appropriate types (number, timestamp, string)
   - Handles null/empty values specially
   - Performs type-specific comparisons
   - Returns `false` to filter out rows that don't match

4. **Special Operators**:
   - `empty` / `nempty`: Checks for null/undefined/empty string
   - `between`: Accepts comma-separated values (e.g., `10,100`)
   - `eq` for text: Performs case-insensitive substring match instead of exact match

#### 4. State Management

The extension saves and restores UI state including:
- Current page and page length
- Column sorting
- Column visibility
- Filter values and operators
- Selected rows
- View mode (table/list)

State is stored in browser's localStorage with configurable duration.

**Deep Linking**: State can be encoded in URL as base64 parameter:
```
/dataset/my-data/resource/123?state=eyJwYWdlIjowLCJzZWFyY2giOnt9fQ==
```

#### 5. Responsive Design

The extension includes two view modes:

- **Table Mode**: Traditional table layout
- **List Mode**: Mobile-friendly card layout showing one record per row with expandable details

Columns can be hidden/shown based on screen size using DataTables' responsive extension.

### Data Flow Diagram

```
User Interaction
    ↓
Filter Input Change Event
    ↓
Is Client-side Filtering Enabled?
    │
    ├─ Yes → Call datatable.draw(false)
    │         ↓
    │         DataTables ext.search function
    │         ↓
    │         Iterate through all rows
    │         ↓
    │         For each column with filter:
    │         - Get filter operator and value
    │         - Convert cell value to correct type
    │         - Perform comparison
    │         - Return false if doesn't match
    │         ↓
    │         All filters passed? → Show row
    │
    └─ No  → Wait for Enter key
              ↓
              Send AJAX request to server
              ↓
              Server queries DataStore
              ↓
              Return filtered results
```

### Why Comparison Operators Only Work with Client-side Filtering

The CKAN DataStore API uses PostgreSQL's full-text search, which:
- Is designed for text searching, not numeric comparisons
- The `filters` parameter only supports exact equality matches
- The `q` parameter is for full-text search queries

To support comparison operators, the extension:
1. Loads all data into the browser (via AJAX endpoint)
2. Stores it in DataTables' internal data structure
3. Implements custom JavaScript filtering logic
4. Filters rows in real-time without server requests

This is why client-side filtering has a row limit (default 10,000) - loading millions of rows into the browser would cause performance issues.

## Differences from Original DataTablesView

| Feature | Original DataTablesView | ckanext-filterview |
|---------|------------------------|-------------------|
| Filtering Type | Server-side only | Server-side OR Client-side |
| Numeric Filters | Exact match only | `=`, `!=`, `>`, `>=`, `<`, `<=` |
| Date Filters | Exact match only | `=`, `!=`, `>`, `>=`, `<`, `<=` |
| Empty Checks | Not supported | `is empty`, `is not empty` |
| Text Filters | Full-text search | Full-text search (server) or substring match (client) |
| Max Dataset Size | Unlimited | 10,000 rows (configurable) for client-side filtering |
| Performance | Good for large datasets | Excellent for small datasets with advanced filters |

## Browser Compatibility

- Chrome/Edge: Full support
- Firefox: Full support (with special handling for ESC key in search inputs)
- Safari: Full support
- Mobile browsers: Supported via responsive mode

## Performance Considerations

**Client-side Filtering**:
- ✅ Pros: Real-time filtering, no server load, supports comparison operators
- ⚠️ Cons: Limited to configured max rows, initial load time, browser memory usage

**Server-side Filtering**:
- ✅ Pros: Handles millions of rows, low browser memory usage
- ⚠️ Cons: Server round-trips on each filter, limited to text search

**Recommendations**:
- Use client-side filtering for datasets < 10,000 rows where comparison operators are needed
- Use server-side filtering for large datasets (>10,000 rows) where simple text search is sufficient
- Adjust `client_side_max_rows` based on your data complexity and user devices

## Troubleshooting

### Comparison operators don't appear
- Ensure "Client Side Filtering" is enabled in the view configuration
- Check that the column type is numeric (int, float, numeric) or date (timestamp, date)
- Text columns use simple text input regardless of client-side filtering setting

### Filtering is slow
- Check the dataset size - if > 10,000 rows, consider server-side filtering
- Disable browser console logs (remove `console.log` statements in production)
- Reduce `client_side_max_rows` if loading too much data

### State not saving
- Check `ckan.datatables.state_saving` is set to `true`
- Verify browser isn't blocking localStorage
- Check `ckan.datatables.state_duration` hasn't expired

### Export includes wrong data
- Filtered exports respect active filters (both view filters and user filters)
- Column visibility affects exported columns
- To export all data, clear filters first

## License

This extension is based on the CKAN DataTablesView plugin.

[AGPL-3.0](https://www.gnu.org/licenses/agpl-3.0.en.html)

## Credits

- Based on [ckanext-datatablesview](https://github.com/ckan/ckanext-datatablesview)
- Built on [DataTables](https://datatables.net/) by SpryMedia Ltd
- Uses [FontAwesome](https://fontawesome.com/) icons
- Internationalization via [DataTables i18n](https://datatables.net/plug-ins/i18n/)

## Contributing

Issues and pull requests are welcome. Please:
- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation
- Test with both Python 2.7 and 3.x
- Test with CKAN 2.9+

## Support

For bugs and feature requests, please open an issue on GitHub.

For CKAN-related questions, see the [CKAN documentation](https://docs.ckan.org/).
