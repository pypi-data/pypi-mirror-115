import time

from lingueeParser import linguee
test = linguee.Linguee(("english", "german"))

test.search('spam')

for i in open('data/wordlist.txt', 'r'):
    print('#' * 20)
    print(i)
    test.search(i)
    open('data/linguee.html', 'wb').write(test.get_response().content)
    time.sleep(5)

