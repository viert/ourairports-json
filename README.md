## OurAirports data in JSON

### What?

If you are into aviation and software development at the same time, you know what you need the most.
You need data. And here it is. The data. Right here in the `output` folder. Feel free to download it, 
it's being updated automatically.

### Why?

The data comes from [ourairports.com](ourairports.com), you might have come across it
already. The problem is, the data there is in `csv` format which makes
it tricky to use without type conversion and extra validation.

Since I was going to use it extensively, I made an automatic JSON generator that you're looking at.

### How?

The data is fetched and parsed every night. If there are changes, they are
committed back to the `output` folder. 

The generator assumes the source files are valid. Since the source is gathered
manually, there might be errors which might lead to generator errors which I will
have to work-around, thus the generator code will evolve and become more stable,
with more data validations etc.

### What's inside?

Supported data models: **airports**, **runways**, **countries** and **navaids**. 
The rest of the datasets will be available later.

### Credits

All credits go to [these guys here](https://ourairports.com/stats/contributors.html).
If you meet one of them make sure to buy them a coffee.
