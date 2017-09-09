CC=clang
CFLAGS=-Wall

db: clean
	$(CC) $(CFLAGS) -o db src/db.c

clean:
	rm -f db bin/*.o