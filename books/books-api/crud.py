######################################
# CRUD sur les différentes tables

from sqlalchemy.orm import Session
import models
import schemas
import hash
from datetime import datetime, timezone
from fastapi import HTTPException

############################################
# Table Reader


def get_reader(db: Session, reader_id: int):
    """
    Récupère un lecteur de la base de données par son identifiant.

    Args:
        db (Session): La session de la base de données utilisée pour l'interaction.
        reader_id (int): L'identifiant unique du lecteur à récupérer.

    Returns:
        models.Reader: Le lecteur correspondant à l'identifiant donné, ou None s'il n'existe pas.
    """
    return db.query(models.Reader).filter(models.Reader.id == reader_id).first()


def get_reader_by_email(db: Session, email: str):
    """
    Récupère un lecteur de la base de données par son adresse email.

    Args:
        db (Session): La session de la base de données utilisée pour l'interaction.
        email (str): L'adresse email du lecteur à rechercher.

    Returns:
        models.Reader: Le lecteur correspondant à l'email donné, ou None s'il n'existe pas.
    """
    return db.query(models.Reader).filter(models.Reader.email == email).first()


def create_reader(db: Session, reader: schemas.ReaderCreate):
    """
    Crée un nouveau lecteur dans la base de données.

    Args:
        db (Session): La session de la base de données utilisée pour l'interaction.
        reader (schemas.ReaderCreate): Les données du lecteur à créer, incluant le nom, prénom, email, et mot de passe.

    Returns:
        models.Reader: Le lecteur nouvellement créé avec les détails enregistrés, y compris l'ID unique généré.
    """
    # hachage du mot de passe avant stockage
    hashed_password = hash.Hash.hash_password(reader.password)
    # création du nouveau reader
    db_reader = models.Reader(
        nom=reader.nom,
        prenom=reader.prenom,
        email=reader.email, hashed_password=hashed_password)
    # ajout du lecteur à la session
    db.add(db_reader)
    # sauvegarde dans la base de données
    db.commit()
    # refresh le lecteur nouvellement créé avec les donées de la base de données (id par exemple)
    db.refresh(db_reader)
    return db_reader

####################################################
# Table Book


def get_books(db: Session):
    """
    Récupère la liste complète des livres de la base de données. On récupère tout ce qui n'est pas optimal si le nombre de livre venait à augmenter

    Args:
        db (Session): La session de la base de données utilisée pour l'interaction.

    Returns:
        List[models.Book]: Une liste de tous les livres dans la base de données.
    """
    return db.query(models.Book).all()


def create_book(db: Session, book: schemas.BookCreate):
    """
    Crée un nouveau livre dans la base de données.

    Args:
        db (Session): La session de la base de données utilisée pour l'interaction.
        book (schemas.BookCreate): Les données du livre à créer, incluant le titre, l'auteur, et l'ISBN.

    Returns:
        models.Book: Le livre nouvellement créé avec les détails enregistrés, y compris l'ID unique généré.
    """
    # crréation de l'instance du modèle Book
    db_book = models.Book(titre=book.titre, auteur=book.auteur, isbn=book.isbn)
    # ajout à la session
    db.add(db_book)
    # sauvegarde dans la base de données
    db.commit()
    # refresh en récupérer les données de la BDD
    db.refresh(db_book)
    return db_book


def get_available_books(db: Session):
    # Récupère les livres qui ne sont pas empruntés ou dont la date de retour n'est pas NULL
    subquery = db.query(models.Loan.book_id).filter(
        models.Loan.date_retour == None).subquery()
    available_books = db.query(models.Book).filter(
        ~models.Book.id.in_(subquery)).all()
    return available_books


########################################################
# Table Loan


def create_loan(db: Session, loan: schemas.LoanCreate):
    """
    Crée un nouvel emprunt de livre pour un lecteur. LA date d'emprunt est automatiquement la date du jour et la date de retour est none car elle sera complétée lors du retour.

    Args:
        db (Session): La session de la base de données utilisée pour l'interaction.
        loan (schemas.LoanCreate): Les données de l'emprunt à créer, incluant l'ID du lecteur, l'ID du livre, et la date d'emprunt.

    Returns:
        models.Loan: L'emprunt nouvellement créé avec les détails enregistrés, y compris l'ID unique généré.
    """
    db_loan = models.Loan(
        reader_id=loan.reader_id,
        book_id=loan.book_id,
        date_emprunt=datetime.now(timezone.utc),
        date_retour=None
    )
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan


def get_loans_by_reader(db: Session, reader_id: int):
    """
    Récupère tous les emprunts d'un lecteur spécifique.

    Args:
        db (Session): La session de la base de données utilisée pour l'interaction.
        reader_id (int): L'identifiant unique du lecteur dont on veut récupérer les emprunts.

    Returns:
        List[models.Loan]: Une liste d'emprunts pour le lecteur donné.
    """
    return db.query(models.Loan).filter(models.Loan.reader_id == reader_id).all()


def get_loan_by_book(db: Session, book_id: int):
    """
    Récupère un emprunt en cours pour un livre spécifique (s'il existe).

    Args:
        db (Session): La session de la base de données utilisée pour l'interaction.
        book_id (int): L'identifiant unique du livre dont on veut vérifier l'emprunt.

    Returns:
        models.Loan: L'emprunt en cours pour le livre donné, ou None s'il n'y a pas d'emprunt en cours.
    """
    return db.query(models.Loan).filter(models.Loan.book_id == book_id).first()


def return_book(db: Session, loan_id: int):
    """ pour rendre un livre"""
    # retrouver l'emprunt dans la base
    try:
        loan = db.query(models.Loan).filter(models.Loan.id == loan_id).first()
        if loan is None:
            raise HTTPException(status_code=404, detail="Loan not found")

        if loan.date_emprunt is None:
            raise HTTPException(
                status_code=400, detail="Loan has no borrow date, cannot return")

        if loan.date_retour is not None:
            raise HTTPException(
                status_code=400, detail="Book has already been returned")

        loan.date_retour = datetime.now(timezone.utc)
        db.commit()
        db.refresh(loan)

        return loan

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred")
