from flask import Flask,render_template,request,session, jsonify
import mysql.connector
from werkzeug.security import generate_password_hash
import time
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = "RAF2025-2026"
CORS(app)

def get_db_connection():
	return mysql.connector.connect(\
		host = 'localhost',
		user = 'root',
		password = '',
		database = 'mydb'
	)

@staticmethod
def proveriDaLiPostojiUsername(username):
	sql_upit = "SELECT * FROM korisnik WHERE username = ?"
	parametri = (username,)
	cursor = mydb.cursor(prepared = True)
	cursor.execute(sql_upit,parametri)
	rez = cursor.fetchone()
	if rez:
		return True
	else:
		return False

@app.route('/products/<product_id>/comment', methods=['POST'])
def addComment(product_id):
    try:
        data = request.get_json()
        mydb = get_db_connection()
        cursor = mydb.cursor(dictionary=True)
        
        sql_upit = """
            INSERT INTO komentar
            (naslov, tekst, Proizvod_ID)
            VALUES (%s, %s, %s)
        """
        data = (
            data['naslov'],
            data['tekst'],
            product_id
        )
        
        cursor.execute(sql_upit, data)
        mydb.commit()
        cursor.close()
        mydb.close()
        
        return jsonify({
            'success': True,
            'message': 'Komentar uspesno dodat!',
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        mydb = get_db_connection()
        cursor = mydb.cursor(dictionary=True)

        vrsta_korisnika = data.get('vrstaKorisnika', '')
        
        if vrsta_korisnika.lower() == 'kupac':
            vrsta_id = 1
        elif vrsta_korisnika.lower() == 'prodavac':
            vrsta_id = 2
        elif vrsta_korisnika.lower() == 'administrator':
            vrsta_id = 3

        # password_hash = generate_password_hash(data['password'])
        
        sql_upit = """
            INSERT INTO korisnik 
            (username, password, email, godinaRodjenja, profilnaSlika, trenutnoStanjeNovca, VrstaKorisnika_id) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        korisnickaData = (
            data['username'],
           	data['password'],
            data['email'],
            data['godinaRodjenja'],
            data.get('profilnaSlika', ''),
            data.get('trenutnoStanjeNovca', 0.0),
            vrsta_id,
        )
        
        cursor.execute(sql_upit, korisnickaData)
        mydb.commit()
        
        cursor.close()
        mydb.close()
        
        return jsonify({
            'success': True,
            'message': 'Korisnik uspesno registrovan!',
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/kupci')
def kupci():
	mydb = get_db_connection()
	cursor = mydb.cursor(dictionary=True)
	cursor.execute("SELECT * FROM Korisnik INNER JOIN VrstaKorisnika ON Korisnik.VrstaKorisnika_ID = VrstaKorisnika.ID WHERE VrstaKorisnika.Naziv = 'kupac';")
	data = cursor.fetchall()
	return jsonify({
		'kupci' : data,
	})

@app.route('/prodavci')
def prodavci():
	mydb = get_db_connection()
	cursor = mydb.cursor(dictionary=True)
	cursor.execute("SELECT * FROM Korisnik INNER JOIN VrstaKorisnika ON Korisnik.VrstaKorisnika_ID = VrstaKorisnika.ID WHERE VrstaKorisnika.Naziv = 'prodavac';")
	data = cursor.fetchall()
	return jsonify({
		'prodavci' : data,
	})

@app.route('/admini')
def admini():
	mydb = get_db_connection()
	cursor = mydb.cursor(dictionary=True)
	cursor.execute("SELECT * FROM Korisnik INNER JOIN VrstaKorisnika ON Korisnik.VrstaKorisnika_ID = VrstaKorisnika.ID WHERE VrstaKorisnika.Naziv = 'administrator';")
	data = cursor.fetchall()
	return jsonify({
		'admini' : data,
	})

@app.route('/kupovine')
def kupovine():
	mydb = get_db_connection()
	cursor = mydb.cursor(dictionary=True)
	cursor.execute('SELECT * FROM kupovina')
	data = cursor.fetchall()
	return jsonify({
		'kupovine' : data,
	})


@app.route('/korisnici')
def korisnici():
	mydb = get_db_connection()
	cursor = mydb.cursor(dictionary=True)
	cursor.execute('SELECT * FROM korisnik')
	data = cursor.fetchall()
	return jsonify({
		'korisnici' : data,
	})

@app.route('/korisnici/<username>')
def dohvatiKorisnikaPoUseru(username):
	mydb = get_db_connection()
	cursor = mydb.cursor(prepared=True)
	cursor.execute(f"SELECT ID FROM korisnik WHERE Username = '{username}'")
	data = cursor.fetchone()
	return jsonify({
		'korisnikID': data[0],
	})

@app.route('/products')
def products():
	mydb = get_db_connection()
	cursor = mydb.cursor(dictionary=True)
	cursor.execute('SELECT * FROM proizvod')
	data = cursor.fetchall()
	return jsonify({
		'proizvodi' : data,
	})

@app.route('/products/add', methods = ['POST'])
def addProduct():
	try:
		data = request.get_json()
		print(data)
		mydb = get_db_connection()
		cursor = mydb.cursor(dictionary=True)
		sql_upit = """INSERT INTO Proizvod
		(naziv,opis,cena,kolicinanastanju,popust)
		VALUES(%s, %s, %s, %s, %s)
		"""
		username = data['username']	

		korisnickaData = (
			data['Naziv'],
			data['Opis'],
			float(data['Cena']),
			int(data['KolicinaNaStanju']),
			float(data['Popust']),
		)

		cursor.execute(sql_upit, korisnickaData)
		mydb.commit()
		proizvodID = cursor.lastrowid
		cursor.execute(f"SELECT ID FROM Korisnik WHERE Username = '{username}'")
		rez = cursor.fetchone()
		korisnikID = rez['ID']
		sql_upit = ("INSERT INTO proizvod_has_korisnik (Proizvod_ID, Korisnik_ID) VALUES (%s,%s)")

		data = (
			int(proizvodID),
			int(korisnikID),
		)

		cursor.execute(sql_upit,data)
		mydb.commit()
		cursor.close()
		mydb.close()

		return jsonify({
            'success': True,
            'message': 'Proizvod uspesno dodat!',
        }), 201
	except Exception as e:
		return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/products/<username>')
def proizvodiProdavca(username):
	mydb = get_db_connection()
	cursor = mydb.cursor(dictionary=True)
	sql_upit = f"""SELECT proizvod.ID, proizvod.Naziv, proizvod.Opis, Cena, KolicinaNaStanju, Popust FROM korisnik 
					INNER JOIN proizvod_has_korisnik
					on korisnik.ID = proizvod_has_korisnik.Korisnik_ID
					INNER JOIN proizvod
					on proizvod_has_korisnik.Proizvod_ID = proizvod.ID 
					WHERE korisnik.Username = '{username}'"""
	print(sql_upit)
	cursor.execute(sql_upit)
	data = cursor.fetchall()
	return jsonify({
		'proizvodi' : data,
	})


@app.route("/comments/<proizvod_id>", methods = ["GET"])
def comments(proizvod_id):
	mydb = get_db_connection()
	cursor = mydb.cursor(dictionary=True)
	sql_upit = f'SELECT * FROM komentar WHERE Proizvod_ID = {proizvod_id}' 
	cursor.execute(sql_upit)
	data = cursor.fetchall()
	return jsonify({
		'komentari' : data,
	})

@app.route('/products/<product_id>/comment/delete/<comment_id>', methods = ["DELETE"])
def obrisiKomentar(product_id,comment_id):
	mydb = get_db_connection()
	cursor = mydb.cursor(prepared=True)
	sql_upit = f"DELETE FROM komentar WHERE ID = {comment_id}"
	cursor.execute(sql_upit)
	mydb.commit()
	return jsonify({
		"Success" : True,
		"Message" : "Komentar uspesno obrisan"
	})

@app.route("/products/delete/<proizvod_id>", methods = ["DELETE"]) 
def deleteProduct(proizvod_id):
	mydb = get_db_connection()
	cursor = mydb.cursor(prepared=True)
	sql_upit = f'DELETE FROM Proizvod WHERE ID = {proizvod_id}'
	cursor.execute(sql_upit)
	mydb.commit()
	return jsonify({
		"Success" : True,
		"Message" : "Proizvod uspesno obrisan"
	})

@app.route('/admin/users')
def adminUsers():
	mydb = get_db_connection()
	cursor = mydb.cursor(dictionary=True)
	sql_upit = "SELECT * FROM korisnik"
	cursor.execute(sql_upit)
	data = cursor.fetchall()
	return jsonify({
		'korisnici': data,
	})

@app.route('/admin/users/update/<user_id>', methods= ["POST", "PUT"])
def AdminUpdateUser(user_id):
	try:
		data = request.get_json()
		mydb = get_db_connection()
		cursor = mydb.cursor(prepared=True)
		sql_upit = """ UPDATE korisnik SET Username = %s, Password = %s, Email = %s, GodinaRodjenja = %s, ProfilnaSlika = %s, TrenutnoStanjeNovca = %s WHERE ID = %s"""
		
		korisnickaData = (
			data['username'],
			data['password'],
			data['email'],
			int(data['godinaRodjenja']),
			data.get('profilnaSlika', ''),
			float(data['trenutnoStanjeNovca']),
			user_id,
		)
			
		cursor.execute(sql_upit, korisnickaData)
		mydb.commit()
		
		cursor.close()
		mydb.close()
		
		return jsonify({
			'success': True,
			'message': 'Korisnik uspesno izmenjen!',
		}), 200
	
	except Exception as e:
		return jsonify({
		'success': False,
		'error': str(e)
	}), 500

@app.route('/products/update/<product_id>', methods = ["POST", "PUT"])
def azurirajProizvod(product_id):
	try:
		data = request.get_json()
		print(data)
		mydb = get_db_connection()
		cursor = mydb.cursor(prepared=True)
		sql_upit = f"""UPDATE proizvod SET Naziv = '{data['Naziv']}', Opis = '{data['Opis']}', Cena = {(data['Cena'])}, KolicinaNaStanju = {data['KolicinaNaStanju']}, Popust = {data['Popust']} WHERE ID = {product_id}"""
		cursor.execute(sql_upit)
		mydb.commit()
		cursor.close()
		mydb.close()
		return jsonify({
				'success': True,
				'message': 'Proizvod uspesno izmenjen!',
			}), 200
	
	except Exception as e:
		return jsonify({
		'success': False,
		'error': str(e)
	}), 500


@app.route('/admin/users/delete/<user_id>', methods = ["DELETE"])
def deleteUser(user_id):
	mydb = get_db_connection()
	cursor = mydb.cursor(prepared=True)
	sql_upit = f"DELETE FROM korisnik WHERE ID = {user_id}"
	cursor.execute(sql_upit)
	mydb.commit()
	return jsonify({
		"Success" : True,
		"Message" : "Korisnik uspesno obrisan"
	})


@app.route('/cart/add', methods = ['POST'])
def cartAdd():
	try:
		data = request.get_json()
		mydb = get_db_connection()
		cursor = mydb.cursor(prepared=True)
		sql_upit = f"""SELECT Cena FROM proizvod WHERE ID = {data['ProizvodID']}"""
		cursor.execute(sql_upit)

		rez = cursor.fetchone()
		cenaProizvoda = float(rez[0])
		UkupnaCena = cenaProizvoda*int(data['Kolicina'])


		sql_upit = f"""SELECT Kolicina FROM proizvod_u_korpi WHERE Proizvod_ID = {data['ProizvodID']} AND Korisnik_ID = {data['KorisnikID']}"""
		cursor.execute(sql_upit)
		row = cursor.fetchone()
		if(row):
			kolicina = int(row[0])+1
			sql_upit = f"""UPDATE proizvod_u_korpi SET Kolicina = {kolicina} WHERE Proizvod_ID = {data['ProizvodID']} AND Korisnik_ID = {data['KorisnikID']}"""
			cursor.execute(sql_upit)
		else:
			sql_upit = """INSERT INTO proizvod_u_korpi (Proizvod_ID, Kolicina, UkupnaCena, Korisnik_ID) 
			VALUES(%s, %s, %s, %s)
			"""

			korisnickaData = (
				data['ProizvodID'],
				int(data['Kolicina']),
				float(UkupnaCena),
				data['KorisnikID'],
			)
			print(korisnickaData)
			cursor.execute(sql_upit,korisnickaData)

		mydb.commit()
		cursor.close()
		mydb.close()
		
		return jsonify({
			'success': True,
			'message': 'Proizvod dodat u korpu',
		}), 201
		
	except Exception as e:
		return jsonify({
			'success': False,
			'error': str(e)
		}), 500


@app.route('/cart/<user_id>')
def cart(user_id):
	mydb = get_db_connection()
	cursor = mydb.cursor(dictionary=True)
	cursor.execute(f"SELECT Naziv, Kolicina, Korisnik_ID, Proizvod_ID FROM proizvod_u_korpi INNER JOIN proizvod on proizvod_u_korpi.Proizvod_ID = proizvod.ID WHERE Korisnik_ID = {user_id}")
	data = cursor.fetchall()
	return jsonify({
		'korpa' : data,
	})

@app.route('/cart/delete/<product_id>', methods = ["DELETE"])
def obrisiIzKorpe(product_id):
	mydb = get_db_connection()
	cursor = mydb.cursor(prepared=True)
	cursor.execute(f"DELETE FROM proizvod_u_korpi WHERE Proizvod_ID = {product_id}")
	mydb.commit()
	return jsonify({
		"Success" : True,
		"Message" : "Obrisano iz korpe"
	})

@app.route('/checkout', methods = ["POST"])
def checkout():
	data = request.get_json()
	mydb = get_db_connection()
	cursor = mydb.cursor(prepared=True)
	UkupnaCena = 0
	korisnik_id = ''
	for stavka in data:
		sql_upit = f"SELECT Cena, Popust FROM proizvod WHERE ID = {stavka['Proizvod_ID']}"
		cursor.execute(sql_upit)
		rez = cursor.fetchone()
		print(rez)
		print(list(rez))
		cena = float(rez[0])
		popust = float(rez[1])
		kolicina = int(stavka['Kolicina'])
		cena = cena*(100-popust)*0.01
		cenaTotal = cena*kolicina
		UkupnaCena += cenaTotal

		sql_upit = f"SELECT TrenutnoStanjeNovca FROM korisnik WHERE ID = {stavka["Korisnik_ID"]}"
		cursor.execute(sql_upit)
		rez = cursor.fetchone()
		korisnik_id = stavka["Korisnik_ID"]
		kupacPare = float(rez[0])
		
		kupacPare = kupacPare-cenaTotal
		sql_upit = f"UPDATE korisnik SET TrenutnoStanjeNovca = {kupacPare} WHERE ID = {stavka["Korisnik_ID"]}"
		cursor.execute(sql_upit)
	
		sql_upit = f"""SELECT korisnik.ID FROM korisnik INNER JOIN proizvod_has_korisnik ON korisnik.ID = proizvod_has_korisnik.Korisnik_ID 
		WHERE proizvod_has_korisnik.Proizvod_ID = {stavka['Proizvod_ID']}"""
		cursor.execute(sql_upit)
		rez = cursor.fetchone()
		prodavacID = int(rez[0])

		sql_upit = f"SELECT TrenutnoStanjeNovca FROM korisnik WHERE ID = {prodavacID}"
		cursor.execute(sql_upit)
		rez = cursor.fetchone()
		prodavacPare = float(rez[0])

		prodavacPare = prodavacPare+cenaTotal
		sql_upit = f"UPDATE korisnik SET TrenutnoStanjeNovca = {prodavacPare} WHERE ID = {prodavacID}"
		cursor.execute(sql_upit)

	sql_upit = f"DELETE FROM proizvod_u_korpi WHERE Korisnik_ID = {stavka["Korisnik_ID"]}"
	cursor.execute(sql_upit)

	korisnik_id = int(korisnik_id)
	sql_upit = f"""INSERT INTO kupovina (DatumKupovine,UkupnaCena,Korisnik_ID) values (CURRENT_DATE(),{UkupnaCena},{korisnik_id})"""
	cursor.execute(sql_upit)

	mydb.commit()

	return jsonify({
		"Success" : True,
		"Message" : "Kupljeno"
	})


@app.route('/kupovine/<user_id>')
def kupovineKorisnik(user_id):
	mydb = get_db_connection()
	cursor = mydb.cursor(dictionary=True)
	sql_upit = f"SELECT * FROM kupovina WHERE Korisnik_ID = {user_id}"
	cursor.execute(sql_upit)
	data = cursor.fetchall()
	return jsonify({
		'kupovine' : data,
	})


app.run(debug=True)


