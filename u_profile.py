import streamlit as st 
import base64
import database as db 




def main(user):
    c1,c2,c3=st.columns([1,2.5,1])
    with c2.container(border=True):
        placeholder=st.empty() 
        user_detail=db.get_one(f"select name,username,image from users where username='{user}'",placeholder)
        st.write(f"""<div style='margin-top: -10px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; height: 100%;'>
                <img src="data:image/png;base64,{base64.b64encode(user_detail[2]).decode()}"  width="150" height="150" style="margin-bottom: 10px; border-radius: 0%; object-fit: cover;"  />
                <p style='margin-bottom: 0px; margin-top: -25px; font-size: 20px;  color:black; font-weight: bold'>{user_detail[0]}</p>
                <p style='margin-bottom: 2px; font-size: 15px; color: grey; '>{user_detail[1]}</p>   
                <br><br>
                """,unsafe_allow_html=True)
        st.write(f"""<div style='margin-top: -10px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; height: 100%;'>
                <p style='margin-bottom: 0px; margin-top: -0px; font-size: 20px;  color:green; font-weight: bold'>Update Details</p>
                """,unsafe_allow_html=True)
        with st.form('ChangeDetail',clear_on_submit=False):
            old_pwd=st.text_input('Old Password',key='p_old')
            new_pwd=st.text_input('New Password',key='p_new')
            confirm=st.text_input('Confirm Password',key='c_new')
            image=st.file_uploader('Change Profile Picture',type=['jpg','jpeg','png'])
            if st.form_submit_button('Update details'):
                place=st.empty()
                if old_pwd.strip():
                    if not new_pwd.strip() or not confirm.strip():
                        place.error('Fill Required Fields')
                    else:
                        if new_pwd == confirm:
                            # Update password in the database
                            db.update_password(user, new_pwd)
                            place.success('Password updated successfully')
                        else:
                            place.error('New password and confirmation do not match')
            elif image:
                # Update profile picture in the database
                db.update_profile_picture(user, image)
                place.success('Profile picture updated successfully')
            elif not old_pwd.strip() and not image:
                place.error('No Details to update')



if __name__=='__main__':
    pass 




