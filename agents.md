# Agent Notes

Lessons learned and implementation notes for AI agents working on this project.

## Excel-DNA Add-in Development

### Packed vs Unpacked XLLs

Excel-DNA produces two types of XLL output:

1. **Unpacked XLLs** (in `bin/Release/net48/`):
   - `FacklerDistributions.xll` and `FacklerDistributions64.xll`
   - Require companion files: `.dna` and `.dll` in the same directory
   - Will fail to load with "FileExists failed when checking for '.dna' file" if .dna is missing
   - Will fail with "External library could not be registered" if .dll is missing

2. **Packed XLLs** (in `bin/Release/net48/publish/`):
   - `FacklerDistributions-packed.xll` and `FacklerDistributions64-packed.xll`
   - Self-contained single files with .dna and .dll embedded
   - **Always use these for distribution**

### Build Script Requirements

When creating a build script for Excel-DNA add-ins:

```powershell
# Copy PACKED versions, not unpacked
$publishDir = "$outputDir\publish"
Copy-Item "$publishDir\*-packed.xll" $distDir -Force

# Rename to remove "-packed" suffix for cleaner distribution
Copy-Item "$publishDir\FacklerDistributions-packed.xll" "$distDir\FacklerDistributions.xll" -Force
Copy-Item "$publishDir\FacklerDistributions64-packed.xll" "$distDir\FacklerDistributions64.xll" -Force
```

### File Naming Conventions

- Do NOT use `-AddIn` suffix in filenames (redundant for .xll files)
- Use consistent naming: `ProjectName.xll` (32-bit) and `ProjectName64.xll` (64-bit)
- Keep only one distribution location (`dist/` folder)

### Common Load Errors

| Error | Cause | Solution |
|-------|-------|----------|
| "FileExists failed when checking for '.dna' file" | Missing .dna file or using unpacked XLL | Use packed XLL from publish folder |
| "External library could not be registered" | Missing .dll file | Use packed XLL or copy .dll alongside |
| Add-in loads but functions don't appear | 32/64-bit mismatch | Use correct XLL for Excel bitness |
| "Enable this add-in?" every time | Windows security blocking | Right-click XLL → Properties → Unblock |

### Project Structure

```
project/
├── excel-addin/
│   ├── FacklerDistributions.csproj
│   ├── FacklerDistributions.dna
│   ├── ExcelFunctions.cs          # Excel UDF wrappers
│   ├── Distributions.cs           # Core math implementation
│   ├── build.ps1
│   └── bin/Release/net48/
│       ├── *.xll, *.dna, *.dll    # Unpacked (don't distribute)
│       └── publish/
│           └── *-packed.xll       # Packed (distribute these)
├── dist/                          # Distribution folder
│   ├── ProjectName.xll            # 32-bit (renamed from packed)
│   ├── ProjectName64.xll          # 64-bit (renamed from packed)
│   └── Demo.xlsx
└── README.md
```

### Required .csproj Settings

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net48</TargetFramework>
    <PlatformTarget>AnyCPU</PlatformTarget>
    <!-- These enable packing -->
    <ExcelDnaPackCompressResources>false</ExcelDnaPackCompressResources>
    <ExcelDnaAllowPackageReferenceResolution>true</ExcelDnaAllowPackageReferenceResolution>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="ExcelDna.AddIn" Version="1.7.0" />
  </ItemGroup>
</Project>
```

### .dna File Template

```xml
<?xml version="1.0" encoding="utf-8"?>
<DnaLibrary Name="Display Name" RuntimeVersion="v4.0" Language="CS">
  <ExternalLibrary Path="ProjectName.dll" ExplicitExports="false" LoadFromBytes="true" Pack="true" />
</DnaLibrary>
```

The `Pack="true"` attribute tells ExcelDnaPack to embed the DLL into the XLL.

### Testing Checklist

Before distributing:
- [ ] Build with `dotnet build --configuration Release`
- [ ] Verify packed XLLs exist in `publish/` folder
- [ ] Copy packed XLLs to `dist/` with clean names
- [ ] Test loading in both 32-bit and 64-bit Excel if possible
- [ ] Verify all functions appear in Excel's function wizard
- [ ] Test a sample function call
