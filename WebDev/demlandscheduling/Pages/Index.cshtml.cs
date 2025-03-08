using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using demlandscheduling.Data;  // Correct namespace for ApplicationDbContext
using demlandscheduling.DataModels;  // Correct namespace for DemlandData

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
