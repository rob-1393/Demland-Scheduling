using Microsoft.EntityFrameworkCore;
using demlandscheduling.Data; //Namespace for ApplicationDbContext
using Serilog;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
// Set up Serilog as the logging provider

builder.Host.UseSerilog((ctx, lc) => lc
    .WriteTo.File("access.log", rollingInterval: RollingInterval.Day)
    .WriteTo.Console());

//Register the DbContext with SQL Server
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));

// Add Razor Pages
builder.Services.AddRazorPages();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error");
    // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
    app.UseHsts();
}

app.UseHttpsRedirection();

app.UseRouting();

app.UseAuthorization();

app.MapStaticAssets();
app.MapRazorPages()
   .WithStaticAssets();

app.Run();
