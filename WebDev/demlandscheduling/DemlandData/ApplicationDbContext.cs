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
//ApplicationDbContext.cs is used as a Entity Framework Core database context. Where it acts as a bridge between the C# and SQL Server Database.
//Thus allowing the Razor Pages to either retrieve, insert, update, delete any data from the database.