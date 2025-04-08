using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using demlandscheduling.Data;
using demlandscheduling.DataModels;
// The above proivdes the necessary components for the Razor Pages, where Microsoft.EntityFrameworkCoore allows interactions within the database.
// While demlandscheduling.Data and demlandscheduling.DataModels is declared to allow the specific database and model classes to be used for the following code.

// Below the PageModel is declared to be part of the Razor Pages Framework.
// Meanwhile, the ApplicationDbContext is responsible for database interactions to be made. Lastly, the _Context stores the database context.
namespace demlandscheduling.Pages.Index  
{
    public class IndexModel(ApplicationDbContext context) : PageModel
    {
        private readonly ApplicationDbContext _context = context;

        public required IList<DemlandData> DemlandDataList { get; set; }  // Required to store a list of DemlandData items that are obtained from the database

        public async Task OnGetAsync()
        {
            // The OnGetAsync data runs when the page is loaded through an HTTP request.
            // It will then proceed with querying the DemlandData table in a asynchronously process. Which lastly, the ToListAsync will then convert the query results into a list.
            DemlandDataList = await _context.DemlandData.ToListAsync();

            // If the DemlandDataList is seen as null, it gets intialized with an empty list
            if (DemlandDataList == null)
            {
                DemlandDataList = new List<DemlandData>();
            }
        }
    }
}
// In Summary the following coding fetches and stores the DemlandData from the database in a asynchronously style, while also ensuring the DemlandDataList properties are intialized properly.