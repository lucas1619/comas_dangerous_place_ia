class Zone:
    def __init__(self, color, geolocalizacion, lugar, tipo_delito, modalidad, suma_x=-1, index=-1):
        self.color = color
        self.geolocalizacion = geolocalizacion
        self.lugar = lugar
        self.tipo_delito = tipo_delito
        self.modalidad = modalidad
        self.suma_x = suma_x
        self.index = index

    def save_to_db(self, conn):
        c = conn.cursor()
        c.execute("INSERT INTO puntos VALUES (?, ?, ?, ?, ?, ?, ?)", (self.index,
                  self.lugar, self.suma_x, self.tipo_delito, self.modalidad, self.geolocalizacion, self.color))
        selected = c.execute("SELECT * FROM puntos")
        print(selected.fetchall())
        conn.commit()
        conn.close()

    def __iter__(self):
        yield 'color', self.color
        yield 'geolocalizacion', self.geolocalizacion
        yield 'lugar', self.lugar
        yield 'tipo_delito', self.tipo_delito
        yield 'modalidad', self.modalidad
        yield 'suma_x', self.suma_x
        yield 'index', self.index

    def __dict__(self):
        return dict(self)
