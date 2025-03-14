using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using demlandscheduling.Data;
using demlandscheduling.DataModels;

namespace demlandscheduling.Pages.Index
{
    public class IndexModel(ApplicationDbContext context) : PageModel
    {
        private readonly ApplicationDbContext _context = context;

        public required IList<DemlandData> DemlandDataList { get; set; }  // No need for nullable if we ensure it is initialized

        public async Task OnGetAsync()
        {
            // Fetch data from the 'DemlandData' table in SQL Server
            DemlandDataList = await _context.DemlandData.ToListAsync();

            // Ensure DemlandDataList is never null
            if (DemlandDataList == null)
            {
                DemlandDataList = new List<DemlandData>();  // Initialize with an empty list if null
            }
        }
    }
}
