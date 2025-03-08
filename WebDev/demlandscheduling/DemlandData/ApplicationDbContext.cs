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

        // Define DbSet for DemlandData
        public DbSet<DemlandData> DemlandData { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            // Configure DemlandData as keyless (if it doesn't have a primary key)
            modelBuilder.Entity<DemlandData>().HasNoKey();
        }
    }
}
