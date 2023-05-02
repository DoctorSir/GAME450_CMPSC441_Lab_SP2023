
# Final Report

## Abstract

This project incorporates various different AI algorithms in varying aspects to create a fully working game using both PyGame as well as the command prompt. 
This also includes algorithms made in class as well as some implemented from scratch using pre-trained models.
Algorithms such as the genetic algorithm for city distribution were able to be adapted into the structure of the main game without much more than minor tweaking.
The journal, however, is a completely new addition to the code based off of GPT-2's text generation to create realistic sounding journal entries about each city from scratch. A link to the pre-trained model used can be found in the Appendix below.

## AI Components

- Genetic Algorithm
- AI Player
- AI Opponent
- Text Generator

## Problems Solved

### Realistic City Distribution

The genetic algorithm mentioned previously takes in a distribution of cities across the map of the game along with the elevation data of the terrain.
Using these two sets of data (along with a fitness function) the algorithm generates a realistic distribution of cities across the map of the game, without having them placed too close together, on the top of a mountain, or underwater.

### Combat

The AI opponent allows the player, whether human or AI, to engage in semi-realistic combat with an algorithm-driven opponent (based on its own health), allowing the player to build a strategy over time.

### Journaling

The text generator allows the game to create journal entries about the cities visited by the player while venturing across the map.
It comes loaded with a few different prompts to allow the name of the city to be the main factor of what text will be generated.
When the journal entry is complete, it is output to the command prompt for the player to read over.

## Appendix

The ChatGPT conversation involving this project can be found [here](https://shareg.pt/OXOdgVE)

The GPT-2 Model can be found [here](https://huggingface.co/gpt2-large)
