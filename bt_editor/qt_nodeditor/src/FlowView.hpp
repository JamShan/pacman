#pragma once

#include <QtWidgets/QGraphicsView>

#include "Export.hpp"

namespace QtNodes
{

class FlowScene;

class  FlowView
  : public QGraphicsView
{
public:

  FlowView(FlowScene *scene);

  QAction* clearSelectionAction() const;

  QAction* deleteSelectionAction() const;

public slots:

  void scaleUp();

  void scaleDown();

  void deleteSelectedNodes();

protected:

  void contextMenuEvent(QContextMenuEvent *event) override;

  void wheelEvent(QWheelEvent *event) override;

  void keyPressEvent(QKeyEvent *event) override;

  void keyReleaseEvent(QKeyEvent *event) override;

  void drawBackground(QPainter* painter, const QRectF& r) override;

  void showEvent(QShowEvent *event) override;

private:

  QAction* _clearSelectionAction;
  QAction* _deleteSelectionAction;

  FlowScene* _scene;
};
}
