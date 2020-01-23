from CreateDataset.CreateDataset import CreateDataset

augment_path = "./train.csv"
test_path = "./test.csv"


def decode(number):
    return label[number]

label = []

dataset = CreateDataset()
x_train, x_test, y_train, y_test = dataset.createdataset(augment_path, test_path)

augment_y = []
for y in y_train:
    augment_y.append(decode(y))

dataset.data_augment(x_train, augment_y)