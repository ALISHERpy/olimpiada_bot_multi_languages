command_start = '/stats'
send_msg = '/send_text'
only_for_admins = 'Sorry, this function is available only for admins. Set "admin" flag in django admin panel.'

secret_admin_commands = f"⚠️ Secret Admin commands\n" \
                        f"{command_start} - bot statistikasi\n"\
                        f"{send_msg} - Userlarga text xabar yuborish\n"\
                        f"/export_users - Userlarni filega saqlab olish\n"\
                        f"/change_id 1515232342 - Natijalar kanal ID o'zgartirish\n"\

users_amount_stat = "<b>Users</b>: {user_count}\n" \
                    "<b>24h active</b>: {active_24}"