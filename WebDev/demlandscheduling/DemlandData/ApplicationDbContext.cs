using Microsoft.EntityFrameworkCore;
using demlandscheduling.DataModels;

namespace demlandscheduling.Data
{
    public class ApplicationDbContext : DbContext
    {
        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
            : base(options)
            {

            }
        public DbSet<CourseData> CourseData {get; set; }
    }
}
