# To use this program, you first need to download the file
# https://nlp.stanford.edu/data/glove.6B.zip
# and extract from it the file
# glove.6B.100d.txt

import tqdm
import math

EmbeddingType = dict[str, list[float]]


def load_embeddings() -> EmbeddingType:
  embeddings = {}
  f = open('glove.6B.100d.txt', encoding='utf8')
  for line in tqdm.tqdm(f, total=400000):
    num_list = line.split()
    word = num_list[0]
    num_list = [float(num) for num in num_list[1:]]
    embeddings[word] = num_list
  return embeddings


def calc_distance(word1: str, word2: str, embeddings: EmbeddingType) -> float:
  sum = 0
  embedding1 = embeddings[word1]
  embedding2 = embeddings[word2]
  for i in range(len(embedding1)):
    num1 = embedding1[i]
    num2 = embedding2[i]
    sum += (num1 - num2) ** 2
  distance = math.sqrt(sum)
  return distance


def find_min_distance(target: str, list_of_words: list[str], embeddings: EmbeddingType) -> tuple[str, float]:
  """Returns the word closest to `target`, and its distance."""
  min_distance = 1000
  closest_word = ""
  for other_word in list_of_words:
    current_dist = calc_distance(target, other_word, embeddings)
    if current_dist < min_distance:
      min_distance = current_dist
      closest_word = other_word
  return (closest_word, min_distance)


def show_distance(word1: str, word2: str, embeddings: EmbeddingType) -> None:
  dist = calc_distance(word1, word2, embeddings)
  print(f'dist({word1}, {word2}) = {dist}')


def main():
  embeddings = load_embeddings()
  # show_distance("cat", "dog", embeddings)
  # show_distance("cat", "lion", embeddings)
  # show_distance("cat", "snail", embeddings)
  # show_distance("cat", "house", embeddings)
  # show_distance("cat", "philosophy", embeddings)
  positive_words = [input("Enter 1 positive word. > ")]
  negative_words = [input("Enter 1 negative word. > ")]
  while True:
    ambiguous_word = input("Enter a word and I will guess if it is positive or negative. > ")
    if ambiguous_word not in embeddings:
      print("Sorry, I do not know that word.")
      continue
    closest_positive_word, positive_distance = find_min_distance(ambiguous_word, positive_words, embeddings)
    closest_negative_word, negative_distance = find_min_distance(ambiguous_word, negative_words, embeddings)
    if positive_distance <= negative_distance:
      is_positive = True
      print(f"I think the word is positive, because it is similar to {closest_positive_word}.")
    else:
      is_positive = False
      print(f"I think the word is negative, because it is similar to {closest_negative_word}.")
    check = input("Am I correct? (y/n) > ")
    if check == "y":
      if is_positive:
        positive_words.append(ambiguous_word)
      else:
        negative_words.append(ambiguous_word)
    if check == "n":
      if is_positive:
        negative_words.append(ambiguous_word)
      else:
        positive_words.append(ambiguous_word)

      

if __name__ == '__main__':
  main()
