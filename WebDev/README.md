# Webdevelopment
Basic Set-Up instructions. Code will have more specific definitions for each line, but this is generally how the connection between the docuemnts work and major setup points that will cause failed website connections if they arent setup to correct names / tables. 

# Appsetting.json
  "ConnectionStrings": {
    "DefaultConnection": "Server=(Your Server Name)\\SQLEXPRESS;Database=(Your Database Name);Trusted_Connection=true (Always set to true) ;MultipleActiveResultSets=true;Encrypt=False (Always set to false for SQL authentication);"

  "AllowedHosts": "*" Allows all hosts. Can specify to your own host, but since its a local connection I dont worry too much, set to your specific server name if you please.


# DemlandDataCS
From the SSMS, we connected the demo table data to the SSMS so that the data can be displayed in the SSMS table. Using SSMS table data, we translated the data into a C# file, using acceptable SQL values.
The reason for this is that the C# file maps to the SSMS table using SQL values and column names. 


# Application Document
Declare path to data models. 
Public DbSet<DemlandData> DemlandData { get; set; } - Maps to the DemlandData.cs to grab from the SSMS table


# Index.cshtml.cs
The User has to map to the correct name spaces for DemlandData amd ApplicationDbContext.

The code below that can be seen in the index creates a string that is connecting and displaying the data model and ApplicationDbContext document, to list the data onto a html page:

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
