import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from pitch import app, db, bcrypt, mail
from pitch.forms import RegistrationForm, LoginForm, UpdateUserForm, PitchForm
from pitch.models import User, Pitch
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message








