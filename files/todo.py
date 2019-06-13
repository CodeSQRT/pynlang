Исходный текст:
ClassName
	__init__ ()
		x = 123
		f = 14
	get ()
		k = 15
		z = 123
		print(123)
		getValue(512)
		TestClass
			__init__ ()
				x = 123
				set (var, a)
					get = set

Преобразованный оптимизатором:
ClassName {
    __init__() {
        x = 123;
        f = 14;
    }
    get() {
        k = 15;
		z = 123;
		print(123);
		getValue(512);
		TestClass {
			__init__() {
				x = 123;
				set(var, a) {
					get = set;
				}
			}
		}
    }
}