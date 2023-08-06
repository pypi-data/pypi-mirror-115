// Experiments in Rust bindings for python code and pipelines dealing with Geo data
// inspired by Ed Wright's blog post: https://www.vortexa.com/insight/integrating-rust-into-python
// and Ed Wright's repo: https://github.com/VorTECHsa/rust-python-integration

use pyo3::prelude::*;
// use rayon::prelude::*;

use geo::algorithm::contains::Contains;
use geo_types::{Coordinate, GeometryCollection, Point};
use geojson::quick_collection;
use geojson::{FeatureCollection, GeoJson};

use std::fs::File;
use std::io::prelude::*;
use std::io::BufReader;

#[pyclass]
struct Engine {
    geo_collection: GeometryCollection<f64>,
    neighborhoods: Vec<String>,
}

#[pymethods]
impl Engine {
    #[new]
    fn new(geojson_fp: &str, property_key: &str) -> Self {
        println!("property key: {}", property_key);
        let geo_file = File::open(geojson_fp).expect("Unable to open file");
        let mut buf_reader = BufReader::new(geo_file);

        let mut geojson_str = String::new();
        buf_reader
            .read_to_string(&mut geojson_str)
            .expect("Unable to read file to string...");

        let geojson_obj = geojson_str.parse::<GeoJson>().unwrap();
        let collection: GeometryCollection<f64> = quick_collection(&geojson_obj).unwrap();

        let json_obj = serde_json::from_str(&geojson_str).unwrap();
        let fc = FeatureCollection::from_json_object(json_obj).unwrap();

        // Get all the target geojson property names and store them in a vector for lookups
        // ie all 'neighbourhood' names or all 'neighbourhoodgroup' names
        let neighborhoods: Vec<String> = fc
            .features
            .iter()
            .map(|feature| match feature.property(property_key) {
                Some(val) => val.as_str().unwrap().to_string(),
                _ => String::from("None found"),
            })
            .collect();

        println!(
            "Built Engine successfully with {} geometries and {} properties",
            &collection.len(),
            &neighborhoods.len()
        );
        println!("neighborhoods: {:?}", &neighborhoods);

        Engine {
            geo_collection: collection,
            neighborhoods,
        }
    }

    fn get_neighborhood(&self, lat: f64, lon: f64) -> String {
        let point = Point(Coordinate { y: lat, x: lon });

        // Iterate through our polygons, stopping at the first hit
        let result = &self
            .geo_collection
            .iter()
            .position(|geo| geo.contains(&point));

        // println!("Found point at position {:?}", &result);

        // Return the name of the neighborhood or Not found
        match result {
            Some(idx) => self.neighborhoods.get(*idx as usize).unwrap().to_owned(),
            None => String::from("Not found"),
        }
    }
}

/// Implements the Python module mr_rogers, registers the class Engine
#[pymodule]
fn mr_rogers(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Engine>()?;

    Ok(())
}
