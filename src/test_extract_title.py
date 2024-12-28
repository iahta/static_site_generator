import unittest
from extract_title import extract_title, generate_pages_recursive

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        markdown = """# Tolkien Fan Club

**I like Tolkien**. Read my [first post here](/majesty) (sorry the link doesn't work yet)

> All that is gold does not glitter

## Reasons I like Tolkien

* You can spend years studying the legendarium and still not understand its depths
* It can be enjoyed by children and adults alike
* Disney *didn't ruin it*
* It created an entirely new genre of fantasy

## My favorite characters (in order)

1. Gandalf
2. Bilbo
3. Sam
4. Glorfindel
5. Galadriel
6. Elrond
7. Thorin
8. Sauron
9. Aragorn

Here's what `elflang` looks like (the perfect coding language):

```
func main(){
    fmt.Println("Hello, World!")
}
```"""
        title = extract_title(markdown)
        self.assertEqual(title, "Tolkien Fan Club")

    def test_generate_pages_recursive(self):
        return generate_pages_recursive("content", "template.html", "public")