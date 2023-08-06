# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [PEP 440](https://www.python.org/dev/peps/pep-0440/) 
and uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.0](https://github.com/ASFHyP3/hyp3-metadata-templates/compare/v1.2.5...v1.3.0)

### Added
* Updated InSAR templates to describe whether the water mask has been applied during phase unwrapping

### Changed
* Updated descriptive language in water mask documentation to include large inland water bodies
* InSAR metadata interfaces to accept a parameter specifying if the water mask has been
  applied during phase unwrapping
  * `--water-mask-applied` argument added to the `insar` argument parser
  * `water_mask_applied` positional argument added to
    * `hyp3_mdatadata.create.create_metadata_file_set_insar`
    * `hyp3_metadata.insar.marshal_metadata`

## [1.2.5](https://github.com/ASFHyP3/hyp3-metadata-templates/compare/v1.2.4...v1.2.5)

### Added
* XML template for the ellipsoid incidence angle GeoTIFF included in the InSAR product package

### Changed
* Updated InSAR README file to add a description of the ellipsoid incidence angle file
* `conda-env.yml` has been renamed to `environment.yml` in-line with community practice

## [1.2.4](https://github.com/ASFHyP3/hyp3-metadata-templates/compare/v1.2.3...v1.2.4)

### Added
* XML template for the water mask GeoTIFF included in the InSAR product package

### Changed
* Updated InSAR README file to add a description of the water mask file

## [1.2.3](https://github.com/ASFHyP3/hyp3-metadata-templates/compare/v1.2.2...v1.2.3)

### Changed
* Minor language edits and addition of RTC Product Guide links to RTC metadata templates
* Additional minor language edits to InSAR metadata templates

## [1.2.2](https://github.com/ASFHyP3/hyp3-metadata-templates/compare/v1.2.1...v1.2.2)

### Changed
* Minor language edits to InSAR metadata templates

## [1.2.1](https://github.com/ASFHyP3/hyp3-metadata-templates/compare/v1.2.0...v1.2.1)

### Fixed
* `create_metadata_file_set_insar` added to `__all__`

## [1.2.0](https://github.com/ASFHyP3/hyp3-metadata-templates/compare/v1.1.0...v1.2.0)

### Added
* Readme file for InSAR products
* `InSarMetadataWriter` class to handle generation of InSar metadata files

### Changed
* Provided different attribution statement options for different uses
* Updated link for new version of the RTC Product Guide 

## [1.1.0](https://github.com/ASFHyP3/hyp3-metadata-templates/compare/v1.0.0...v1.1.0)
### Changed
- Added DB option to RTC Readme

## [1.0.0](https://github.com/ASFHyP3/hyp3-metadata-templates/compare/v0.4.2...v1.0.0)

### Changed
* creation of rtc metadata files moved to `rtc.py`
* `create.create_metadata_file_set` renamed to `create.create_metadata_file_set_rtc`

## [0.4.2](https://github.com/ASFHyP3/hyp3-metadata-templates/compare/v0.4.1...v0.4.2)

### Added
* Additional RGB Decomposition info in the color browse xml template

### Changed
* Scattering area map metadata now correctly lists the radiometry as gamma-0 instead of the radiometry parameter
  specified for the RTC output
* Updated formatting of URL links in xml files so that they open in a separate browse window when clicked in ArcGIS Pro

## [0.4.1](https://github.com/ASFHyP3/hyp3-metadata-templates/compare/v0.4.0...v0.4.1)

### Added
* Additional info in Copernicus DEM GLO-30 xml template

### Changed
* Sentinel-1 mission URL in all templates (resolves [#58](https://github.com/ASFHyP3/hyp3-metadata-templates/issues/58))
* The expected dem name value for Copernicus DEM GLO-30 is now `GLO-30` for:
  * `dem_name` parameter to `hyp3_metadata.create_metadata_file_set()`
  * `--dem-name` parameter to `hyp3_metadata` entrypoint

### Removed
* Reference to geocoded products from hyp3.asf.alaska.edu from all xml templates other than `product.xml.j2`

## [0.4.0](https://github.com/ASFHyP3/hyp3-metadata-templates/compare/v0.3.0...v0.4.0)

### Added
* Package level script to generate an example set of metadata for a product;
  see [the README](README.md) for usage.
* `_rgb.xml` ArcGIS metadata file is now generated for RTC products that include an RGB decomposition GeoTIFF.
* RTC product README now includes a description of the optional RGB decomposition GeoTIFF.

### Changed
* Environment name in `conda-env.yml` has been changed to `hyp3-metadata-templates` to match the project name.

## [0.3.0](https://github.com/ASFHyP3/hyp3-metadata-templates/compare/v0.2.0...v0.3.0)

### Added
* Draft `_dem.tif.xml` template for the Copernicus 30m global DEM.

### Changed
* RTC readme now includes more detail regarding the packaged DEM.

## [0.2.0](https://github.com/ASFHyP3/hyp3-metadata-templates/compare/v0.1.4...v0.2.0)

### Added
* [IFSAR](https://www.usgs.gov/centers/eros/science/usgs-eros-archive-digital-elevation-interferometric-synthetic-aperture-radar)
  DEM (DSM version only) is now supported

### Changed
* Product README will only include information about the specific DEM used
* For unsupported (unknown) DEMs
  * no `_dem.tif.xml` will be created
  * DEM resolution will be set to `UNKNOWN`
  * No DEM blurb nor any references to `_dem.tif.xml` will be included in the product README

## [0.1.4](https://github.com/ASFHyP3/hyp3-metadata-templates/compare/v0.1.3...v0.1.4)

### Changed
* Use past tense when describing scattering area cell value calculations to clarify that they reflect the
  user-provided radiometry

## [0.1.3](https://github.com/ASFHyP3/hyp3-metadata-templates/compare/v0.1.2...v0.1.3)

### Added
* Added documentation for the new scattering area map generated by RTC GAMMA:
  * Added layer description to readme
  * Added an ArcGIS-compatible xml file

### Removed
* Removed description of .iso.xml file eliminated in hyp3-rtc-gamma v2.3.0.

## [0.1.2](https://github.com/ASFHyP3/hyp3-metadata-templates/compare/v0.1.1...v0.1.2)

### Changed
- Lineage statements now include the processing year when referring to HyP3, e.g. `ASF DAAC HyP3 2020`

## [0.1.1](https://github.com/ASFHyP3/hyp3-metadata-templates/compare/v0.1.0...v0.1.1)

### Fixed
* `hyp3_metadata.create_metadata_file_set` now creates metadata for color browse images (`*_rgb.png`)
* Thumbnail images in XML files are correctly encoded

## [0.1.0](https://github.com/ASFHyP3/hyp3-metadata-templates/compare/v0.0.0...v0.1.0)

### Added
* `hyp3_metadata.create_metadata_file_set` method to create all standard metadata files for HyP3 products
  
  *Note: this only currently supports RTC products created with the GAMMA processor.*

### Changed
* Now a pip-installable python package called `hyp3_metadata`
