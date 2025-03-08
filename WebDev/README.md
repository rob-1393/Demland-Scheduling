# Webdevelopment
Ken and Max
#DemlandDataCS
From the SSMS, we connected the demo table data to the SSMS so that the data can be displayed in the SSMS table. Using SSMS table data, we translated the data into a C# file, using acceptable SQL values.
The reason for this is that the C# file maps to the SSMS table using SQL values and column names. 

#Application Document
Declare path to data models. 
Public DbSet<DemlandData> DemlandData { get; set; } - Maps to the DemlandData.cs to grab from the SSMS table

#Index.cshtml.cs
The User has to map to the correct name spaces for DemlandData amd ApplicationDbContext.

namespace demlandscheduling.Pages.Courses
{
    public class IndexModel : PageModel
    {
        private readonly ApplicationDbContext _context;

        public IndexModel(ApplicationDbContext context)
        {
            _context = context;
        }

        public IList<DemlandData>? DemlandDataList { get; set; }  // Change to DemlandDataList

        public async Task OnGetAsync()
        {
            // Fetch data from the 'DemlandData' table in SQL Server
            DemlandDataList = await _context.DemlandData.ToListAsync();  // Query from DemlandData table
        }
    }
}
