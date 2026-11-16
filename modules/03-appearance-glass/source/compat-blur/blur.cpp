// SPDX-License-Identifier: GPL-2.0-or-later
#include <kwineffects.h>
#include <kwinglutils.h>
#include <epoxy/gl.h>
#include <xcb/xcb.h>
#include <QDebug>
#include <KConfigGroup>
#include <KWindowSystem>
#include <cstring>
using namespace KWin;
class AetherBlur: public Effect {
 Q_OBJECT
 float radiusScale=1;
 struct Buffers{GLuint tx[2]={0,0};int width=0,height=0;}; QHash<EffectWindow*,Buffers> buffers;
 GLuint program=0,fbo=0;long atom=0;
 GLuint shader(GLenum type,const char *text){GLuint s=glCreateShader(type);glShaderSource(s,1,&text,nullptr);glCompileShader(s);GLint ok;glGetShaderiv(s,GL_COMPILE_STATUS,&ok);if(!ok){char msg[2048];glGetShaderInfoLog(s,sizeof(msg),nullptr,msg);qWarning()<<msg;}return s;}
 bool target(EffectWindow*w){return !w->isDeleted()&&!w->isDesktop()&&!w->readProperty(atom,XCB_ATOM_CARDINAL,32).isNull();}
 void quad(){glBegin(GL_QUADS);glTexCoord2f(0,0);glVertex2f(-1,-1);glTexCoord2f(1,0);glVertex2f(1,-1);glTexCoord2f(1,1);glVertex2f(1,1);glTexCoord2f(0,1);glVertex2f(-1,1);glEnd();}
public:
 void reconfigure(ReconfigureFlags)override{auto config=KSharedConfig::openConfig("kwinrc");config->reparseConfiguration();radiusScale=qBound(1,KConfigGroup(config,"Effect-blur").readEntry("BlurStrength",8),15)/8.f;effects->addRepaintFull();}
 AetherBlur(){
 reconfigure(ReconfigureAll);
 atom=effects->announceSupportProperty(QByteArrayLiteral("_KDE_NET_WM_BLUR_BEHIND_REGION"),this);
 const char* vs="#version 120\nvoid main(){gl_Position=gl_Vertex;gl_TexCoord[0]=gl_MultiTexCoord0;}";
 const char* fs="#version 120\nuniform sampler2D tex;uniform vec2 stepSize;void main(){vec4 c=vec4(0.); for(int i=-8;i<=8;i++){c+=texture2D(tex,gl_TexCoord[0].xy+float(i)*stepSize);}gl_FragColor=c/17.;}";
 effects->makeOpenGLContextCurrent();program=glCreateProgram();GLuint v=shader(GL_VERTEX_SHADER,vs),f=shader(GL_FRAGMENT_SHADER,fs);glAttachShader(program,v);glAttachShader(program,f);glLinkProgram(program);glDeleteShader(v);glDeleteShader(f);GLint ok;glGetProgramiv(program,GL_LINK_STATUS,&ok);if(!ok){qWarning()<<"Aether blur link failed";glDeleteProgram(program);program=0;}glGenFramebuffers(1,&fbo);connect(effects,&EffectsHandler::windowDeleted,this,[this](EffectWindow*w){effects->makeOpenGLContextCurrent();auto i=buffers.find(w);if(i!=buffers.end()){glDeleteTextures(2,i.value().tx);buffers.erase(i);}});effects->addRepaintFull();
 }
 ~AetherBlur()override{effects->makeOpenGLContextCurrent();for(auto &b:buffers)glDeleteTextures(2,b.tx);glDeleteFramebuffers(1,&fbo);if(program)glDeleteProgram(program);effects->addRepaintFull();}
 bool isActive()const override{return program!=0;}
 int requestedEffectChainPosition()const override{return 20;}
 void prePaintScreen(ScreenPrePaintData&data,std::chrono::milliseconds time)override{
 // Backdrop copies must never sample the previous frame's window contents.
 data.paint |= effects->virtualScreenGeometry();
 effects->prePaintScreen(data,time);
 }
 void prePaintWindow(EffectWindow*w,WindowPrePaintData&data,std::chrono::milliseconds time)override{
 effects->prePaintWindow(w,data,time);if(!KWindowSystem::showingDesktop()&&target(w)){data.setTranslucent();data.opaque=QRegion();}
 }
 void drawWindow(EffectWindow*w,int mask,const QRegion&region,WindowPaintData&data)override{
 if(program&&!KWindowSystem::showingDesktop()&&target(w)&&data.xScale()==1&&data.yScale()==1){
 QRect screen=effects->renderTargetRect();QRect r=w->frameGeometry().toAlignedRect().intersected(screen);
 if(r.width()>2&&r.height()>2){
 GLint oldProgram,oldActive,oldTex,oldFbo,oldRead,view[4],oldReadBuffer,oldDrawBuffer,oldScissor[4];
 glGetIntegerv(GL_SCISSOR_BOX,oldScissor);glGetIntegerv(GL_CURRENT_PROGRAM,&oldProgram);glGetIntegerv(GL_ACTIVE_TEXTURE,&oldActive);glActiveTexture(GL_TEXTURE0);glGetIntegerv(GL_TEXTURE_BINDING_2D,&oldTex);glGetIntegerv(GL_DRAW_FRAMEBUFFER_BINDING,&oldFbo);glGetIntegerv(GL_READ_FRAMEBUFFER_BINDING,&oldRead);glGetIntegerv(GL_VIEWPORT,view);glGetIntegerv(GL_READ_BUFFER,&oldReadBuffer);glGetIntegerv(GL_DRAW_BUFFER,&oldDrawBuffer);
 GLboolean blend=glIsEnabled(GL_BLEND),scissor=glIsEnabled(GL_SCISSOR_TEST),srgb=glIsEnabled(GL_FRAMEBUFFER_SRGB);glDisable(GL_BLEND);glDisable(GL_SCISSOR_TEST);glDisable(GL_FRAMEBUFFER_SRGB);
 auto &b=buffers[w];if(!b.tx[0])glGenTextures(2,b.tx);auto &tx=b.tx;int &tw=b.width,&th=b.height;
 const int width=r.width(),height=r.height();
 if(tw!=width||th!=height){tw=width;th=height;for(GLuint t:tx){glBindTexture(GL_TEXTURE_2D,t);glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA8,tw,th,0,GL_RGBA,GL_UNSIGNED_BYTE,nullptr);glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR);glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR);glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S,GL_CLAMP_TO_EDGE);glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T,GL_CLAMP_TO_EDGE);}}
 glBindFramebuffer(GL_READ_FRAMEBUFFER,oldFbo);glReadBuffer(oldFbo?GL_COLOR_ATTACHMENT0:GL_BACK);glBindTexture(GL_TEXTURE_2D,tx[0]);glCopyTexSubImage2D(GL_TEXTURE_2D,0,0,0,r.x()-screen.x(),screen.height()-(r.y()-screen.y())-height,width,height);
 glUseProgram(program);glUniform1i(glGetUniformLocation(program,"tex"),0);
 glBindFramebuffer(GL_DRAW_FRAMEBUFFER,fbo);glFramebufferTexture2D(GL_DRAW_FRAMEBUFFER,GL_COLOR_ATTACHMENT0,GL_TEXTURE_2D,tx[1],0);glDrawBuffer(GL_COLOR_ATTACHMENT0);glViewport(0,0,width,height);glUniform2f(glGetUniformLocation(program,"stepSize"),radiusScale/width,0);quad();
 glBindFramebuffer(GL_DRAW_FRAMEBUFFER,oldFbo);glDrawBuffer(oldDrawBuffer);glViewport(r.x()-screen.x(),screen.height()-(r.y()-screen.y())-height,width,height);glBindTexture(GL_TEXTURE_2D,tx[1]);glUniform2f(glGetUniformLocation(program,"stepSize"),0,radiusScale/height);
 // Preserve the window's blur mask, including rounded tooltip corners.
 QRegion shape;const QByteArray prop=w->readProperty(atom,XCB_ATOM_CARDINAL,32);
 if(prop.size()>0&&prop.size()%16==0){for(int i=0;i<prop.size();i+=16){quint32 a[4];std::memcpy(a,prop.constData()+i,16);shape+=QRect(a[0],a[1],a[2],a[3]).translated(w->frameGeometry().topLeft().toPoint());}}else shape=r;
 shape&=r;shape&=region;glEnable(GL_SCISSOR_TEST);for(const QRect&clip:shape){glScissor(clip.x()-screen.x(),screen.height()-(clip.y()-screen.y())-clip.height(),clip.width(),clip.height());quad();}
 glUseProgram(oldProgram);glBindTexture(GL_TEXTURE_2D,oldTex);glActiveTexture(oldActive);glBindFramebuffer(GL_READ_FRAMEBUFFER,oldRead);glReadBuffer(oldReadBuffer);glBindFramebuffer(GL_DRAW_FRAMEBUFFER,oldFbo);glDrawBuffer(oldDrawBuffer);glViewport(view[0],view[1],view[2],view[3]);glScissor(oldScissor[0],oldScissor[1],oldScissor[2],oldScissor[3]);if(blend)glEnable(GL_BLEND);if(!scissor)glDisable(GL_SCISSOR_TEST);if(srgb)glEnable(GL_FRAMEBUFFER_SRGB);
 }
 }
 effects->drawWindow(w,mask,region,data);
 }
};
KWIN_EFFECT_FACTORY_SUPPORTED_ENABLED(AetherBlur,"metadata.json",return effects->isOpenGLCompositing();,return false;)
#include "blur.moc"
