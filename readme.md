# Barbot Library

## Development
To begin, ensure that your system has python v3 installed, and pip installed.
Then, install the dependencies with....
```
pip install -r requirements.txt
```

Now, to run the application...
```
python app/main.py
```


## Spec
Barbot uses a JSON formatted spec to configure drink jobs and system settings. 

System Settings 
```
{
    // the pin of the scale
    "weight_pin": "43",

    // the offset of the scale, to account for future error. 
    //  the actual weight will always be calculated as the weight
    //  reported by the scale, plus the `weight_offset`
    "weight_offset": "0",

    // an array of ingredients configurations
    "ingredients": [
        {
            // the pin of the pump holding Jack
            "pin_id": "44",

            // the name of the drink
            "name": "Jack Daniels",

            // the density of the drink (used to back-calculate volume)
            "density": "1"
        },
        {
            // the pin of the pump holding Coke
            "pin_id": "45",

            // the name of the drink
            "name": "Coke",

            // the density of the drink (used to back-calculate volume)
            "density": "1"
        }
    ]
}
```

Drink Configuration
```
{
    // the name of the beverage
    "name": "Jack n Coke",

    // a description for the beverage
    "description": "The staple of modern civilization",

    // the ordered set of steps for creating the beverage
    "components": [
        {
            // the name of the Jack
            "name": "Jack Daniels",

            // how much 
            "volume": "1"
        },
        {
            // the name of the Coke
            "name": "Coke",

            // how much
            "volume": "2"
        }
    ]
}
```

Using the above spec, a Barbot can be configured to create any mix drink that is a composition of available ingredients. The BartenderMan will have one `System Settings` spec, and several `Drink Configuration` specs. A `/config` directory will hold these files in the following layout,

```
    /config
        system_spec.json
        /drinks
            jack_n_code.json
            gin_n_tonic.json
            shirley_temply.json
```