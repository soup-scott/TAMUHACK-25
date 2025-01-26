import React from 'react';
import data from './test.json';
import './style/GenCars.css'; // Import the CSS file

const GenCars = () => {
    const carsArray = Object.values(data); // Ensure carsArray is defined

    return (
        <div className="all-cars-container">
            <h1>SUGGESTED VEHICLES</h1>
            <div className="cars-grid">
                {carsArray.map((car, index) => (
                    <div key={index} className="car-card">
                        <h2>{car["Display_Name"]}</h2>
                        <img
                            src={car.ImageURL}
                            alt={car["Display_Name"]}
                            className="car-image"
                        />
                        <h3>MSRP: {car.MSRP}</h3>
                        <h3>Seating: {car.Seating}</h3>
                        <h3>Avg MPG/Range: {car.Range ? car.Range : car.Combined_Mileage}</h3>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default GenCars;