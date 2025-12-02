from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Projecte, Aportacio
import os

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crowdfunding.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'devsecret123')
    db.init_app(app)
    return app

app = create_app()

@app.route('/')
def index():
    projectes = Projecte.query.order_by(Projecte.data_inici.desc()).all()
    return render_template('index.html', projectes=projectes)

@app.route('/crear', methods=['GET', 'POST'])
def crear_projecte():
    if request.method == 'POST':
        titol = request.form.get('titol')
        descripcio = request.form.get('descripcio')
        objectiu = float(request.form.get('objectiu') or 100)
        minim_per_donacio = float(request.form.get('minim_per_donacio') or 1)
        maxim_per_donant = float(request.form.get('maxim_per_donant') or 50)
        maxim_projecte = float(request.form.get('maxim_projecte') or 200)

        projecte = Projecte(
            titol=titol,
            descripcio=descripcio,
            objectiu=objectiu,
            minim_per_donacio=minim_per_donacio,
            maxim_per_donant=maxim_per_donant,
            maxim_projecte=maxim_projecte
        )
        db.session.add(projecte)
        db.session.commit()
        flash('Projecte creat correctament.', 'success')
        return redirect(url_for('index'))

    return render_template('crear_projecte.html')

@app.route('/projecte/<int:projecte_id>')
def veure_projecte(projecte_id):
    projecte = Projecte.query.get_or_404(projecte_id)
    # calcular percentatge
    percentatge = min(100, (projecte.recaptat / projecte.maxim_projecte) * 100 if projecte.maxim_projecte else 0)
    return render_template('projecte.html', projecte=projecte, percentatge=percentatge)

@app.route('/projecte/<int:projecte_id>/aportar', methods=['GET', 'POST'])
def aportar(projecte_id):
    projecte = Projecte.query.get_or_404(projecte_id)
    if request.method == 'POST':
        nom = request.form.get('nom').strip()
        try:
            quant = float(request.form.get('quantitat'))
        except (ValueError, TypeError):
            flash('Introdueix una quantitat vàlida.', 'danger')
            return redirect(request.url)

        # Validacions
        if quant < projecte.minim_per_donacio:
            flash(f'La donació mínima per transacció és {projecte.minim_per_donacio} EGLD.', 'danger')
            return redirect(request.url)

        # total aportat per aquest usuari al projecte
        aportats_user = db.session.query(db.func.sum(Aportacio.quantitat)).filter_by(projecte_id=projecte.id, usuari=nom).scalar() or 0.0
        if aportats_user + quant > projecte.maxim_per_donant:
            flash(f'No pots aportar. Aquest usuari superaria el màxim per donant ({projecte.maxim_per_donant} EGLD).', 'danger')
            return redirect(request.url)

        # max total projecte
        if projecte.recaptat + quant > projecte.maxim_projecte:
            flash('No es pot acceptar la donació: s\'excediria el màxim del projecte.', 'danger')
            return redirect(request.url)

        # Tot ok: guardar aportació
        aport = Aportacio(projecte_id=projecte.id, usuari=nom, quantitat=quant)
        projecte.recaptat += quant
        db.session.add(aport)
        db.session.commit()
        flash('Gràcies per la teva aportació!', 'success')
        return redirect(url_for('veure_projecte', projecte_id=projecte.id))

    return render_template('aportar.html', projecte=projecte)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
