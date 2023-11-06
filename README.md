# Art from genomes
I was interested about seeing how genomes looked. So decided to make it into an art project :p. But this will take the provided genome file and load it into memory (bad idea ik) and get its length and make a square image with the resolution of sqrt(genome_lengt) and then loop trough the genome and assign a color to each dna thingy (A, T, G C) and put the color on the square image. It loops over the image array from left to right, top to bottom and buts the color in its corresponding location. Really not accurate, but its cool to see some patterns emerging from the image.

example(vaccinia virus genome):
<br>
![vaccinia virus](vaccina_genome.png)
(you can see kind of some vertical lines)

TODO: Will maybe try adding multithreading, because as we all know, multithreading makes code 100x better
<br>
TODO: Parse the genome? files better. The current way is shit
<br>
TODO: Make a better image viewer? Maybe the ability to zoom and pan around (plotting it for now. makes the image a bit blurry but oh well ```-\_(-_-)_/-```)
