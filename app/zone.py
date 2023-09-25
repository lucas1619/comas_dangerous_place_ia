class Zone: 
    def __init__(self, color, geolocalizacion, lugar, suma_x = -1, index = -1):
        self.color = color
        self.geolocalizacion = geolocalizacion
        self.lugar = lugar
        self.suma_x = suma_x
        self.index = index

    def save_to_db(self, conn):
        c = conn.cursor()
        c.execute("INSERT INTO puntos VALUES (?, ?, ?, ?, ?)", (self.index, self.lugar, self.suma_x, self.geolocalizacion, self.color))
        conn.commit()
        conn.close()
    
    def __iter__(self):
        yield 'color', self.color
        yield 'geolocalizacion', self.geolocalizacion
        yield 'lugar', self.lugar
        yield 'suma_x', self.suma_x
        yield 'index', self.index

    def __dict__(self):
        return dict(self)