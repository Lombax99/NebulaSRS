variable "rg_name" {
  type    = string
  default = "srs2024-stu-g2"
}

variable "location" {
  type    = string
  default = "West Europe"
}

#Credenziali google per mandare mail per l'autenticazione a due fattori
#- Forse credenziali del superuser
variable "google_username" {
  sensitive = true
}
variable "google_password" {
  sensitive = true
}

#Define variables for DB (username, password, host, pgdb)
variable "db_username" {
  sensitive = true
}
variable "db_password" {        
  sensitive = true
}
variable "db_host" {
  sensitive = true
}
variable "db_pgdb" {
  sensitive = true
}

#Segreto di Flask-BCrypt
variable "flask_secret" {
  sensitive = true
}

# Set secrets via environment variables
# When you run Terraform, it'll pick up the secrets automatically
#export TF_VAR_google_username=(the username)
#export TF_VAR_google_password=(the password)
#export TF_VAR_db_username=(the username)
#export TF_VAR_db_password=(the password)
#export TF_VAR_db_host=(the host)
#export TF_VAR_db_pgdb=(the pgdb)
#export TF_VAR_flask_secret=(the secret)
#terraform apply