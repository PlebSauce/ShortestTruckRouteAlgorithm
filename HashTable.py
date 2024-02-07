# HashTable.py
# Citing Source: W-3_ChainingHashTable_zyBooks_Key-Value_CSV_Greedy_Dijkstra.py
class HashTable:
    # initializing hash table of size 40
    def __init__(self, initial_capacity=40):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    def insert(self, key, value):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for pair in bucket_list:
            if pair[0] == key:
                pair[1] = value
                return True

        key_value_pair = [key, value]
        bucket_list.append(key_value_pair)
        return True

    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        if key in bucket_list:
            bucket_list.remove(key)

    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for pair in bucket_list:
            if pair[0] == key:
                return pair[1]
        return None

    # print method may not be used, mostly for debugging purposes
    def print(self):
        print(HashTable)
        for item in self.table:
            if item is not None:
                print(str(item))
