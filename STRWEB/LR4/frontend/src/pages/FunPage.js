import React from 'react';
import DogImage from '../components/DogImage';
import IPAddress from '../components/IPAddress';

const FunPage = () => {
    return (
        <div className="container">
            <h1>Веселые штуки</h1>
            <IPAddress />
            <DogImage />
        </div>
    );
};

export default FunPage;